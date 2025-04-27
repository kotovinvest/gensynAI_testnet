import logging
import time
from collections import defaultdict
from typing import Sequence

import hivemind_exp.gsm8k.stage1_rewards as stage1_rewards
import hivemind_exp.gsm8k.stage2_rewards as stage2_rewards
import hivemind_exp.gsm8k.stage3_rewards as stage3_rewards
from hivemind_exp.dht_utils import (
    DHT,
    HivemindNode,
    get_dht_value,
    get_outputs,
    rewards_key,
)
from hivemind_exp.gsm8k.generate_prompts import get_stage2_samples, get_stage3_samples
from hivemind_exp.gsm8k.stage_merger import (
    Any,
    merge_stage1_question,
    merge_stage2_question,
)
from hivemind_exp.hivemind_utils import SingleStageData, StageData


def merged_prev_stage_datasets(
    dht: DHT,
    node: HivemindNode,
    r: int,
    s: int,
    merge_fn,
    samples_fn,
    dht_sample_limit = 200,
    check_interval: float = 5,
    wait_timeout: float = 10,
    log_tag=None,
):
    if not log_tag:
        log_tag = node.key

    logger = logging.getLogger(f"{__name__}:{log_tag}")

    merged_qs = []

    # Retrieves and merges last stage samples locally and from DHT.
    def get_prev_rewards():
        return get_dht_value(
            dht, key=rewards_key(r, s - 1), beam_size=100
        )

    prev_rewards: dict[str, Any] | None = get_prev_rewards()
    start_time = time.monotonic()
    while not prev_rewards and time.monotonic() - start_time < wait_timeout:
        logger.info(
            f"Can't retrieve round {r} stage {s - 1} rewards; trying again in {check_interval}s "
        )
        time.sleep(check_interval)
        prev_rewards = get_prev_rewards()

    # Add the current node's local samples first.
    prev_items: dict[str, list] = defaultdict(list)
    try:
        prev_node_outputs = get_outputs(dht, node.key, r, s - 1, node.get_stage_outputs)
        for item in prev_node_outputs.items():
            prev_items[node.key].append(item)
    except ValueError:
        # Joined after the round has started.
        logger.info(f"Could not retrieve local outputs for round {r} stage {s - 1}")

    # Add other nodes' samples iff rewards are available.
    if prev_rewards:
        node_keys = prev_rewards.keys()
        dht_sample_count = 0
        for node_key in node_keys:
            if dht_sample_count > dht_sample_limit:
                break

            if node_key == node.key:
                continue
            try:
                prev_node_outputs = get_outputs(dht, node_key, r, s - 1)
                for item in prev_node_outputs.items():
                    prev_items[node_key].append(item)

                    dht_sample_count += 1
                    if dht_sample_count > dht_sample_limit:
                        break

            except ValueError:
                # Skip this node's answers for the current round and stage.
                logger.debug(
                    f"Found rewards published for node: {node_key} but no outputs!"
                )

    # Group samples by question hash.
    q_to_keyed_items: dict[str, dict[str, Any]] = defaultdict(dict)
    for node_key, items in prev_items.items():
        for item in items:
            q_hash, (_, outputs) = item
            q_to_keyed_items[q_hash][node_key] = outputs

    # Merge sample lists.
    for outputs in q_to_keyed_items.values():
        merged = merge_fn(outputs)
        merged_qs.append(merged)

    return samples_fn(merged_qs)


def gsm8k_stage_data(
    dht: DHT,
    node: HivemindNode,
    initial_train_dataset,
    initial_test_dataset,
    check_interval: float = 5,
    log_tag=None,
):
    def cumulative_reward_0(**kwargs):
        return stage1_rewards.hivemind_cumulative_reward(node, **kwargs)

    def cumulative_reward_1(**kwargs):
        return stage2_rewards.hivemind_cumulative_reward(node, **kwargs)

    def cumulative_reward_2(**kwargs):
        return stage3_rewards.hivemind_cumulative_reward(node, **kwargs)

    def stage2_datasets_fn(r, s):
        return merged_prev_stage_datasets(
            dht,
            node,
            r,
            s,
            merge_stage1_question,
            get_stage2_samples,
            check_interval=check_interval,
            log_tag=log_tag,
        )

    def stage3_datasets_fn(r, s):
        return merged_prev_stage_datasets(
            dht,
            node,
            r,
            s,
            merge_stage2_question,
            get_stage3_samples,
            check_interval=check_interval,
            log_tag=log_tag,
        )

    def round_winners(limit=10) -> Sequence[str]:
        final_stage_outputs, _ = merged_prev_stage_datasets(
            dht,
            node,
            node.round_num,
            3,
            lambda x: x,
            lambda v: (v, v),
            check_interval=check_interval,
            log_tag=log_tag,
        )
        logger = logging.getLogger(f"{__name__}:{log_tag}")

        rewards = defaultdict(float)
        for outputs in final_stage_outputs:
            for node_key, output in outputs.items():
                question = output.get("question")
                faulty_completion = False
                if question is None:
                    logger.warning(f"Missing 'question' key in output: {output}")
                    output["question"] = "<no question available>"
                    faulty_completion = True
                stage3_prompt = output.get("stage3_prompt")
                if stage3_prompt is None:
                    logger.warning(f"Missing 'stage3_prompt' key in output: {output}")
                    output["stage3_prompt"] = "<no stage3 prompt available>"
                    faulty_completion = True
                final_answer = output.get("final_agent_decision")
                if final_answer is None:
                    logger.warning(f"Missing 'final_agent_decision' key in output: {output}")
                    output["final_agent_decision"] = "<no final agent decision available>"
                    faulty_completion = True
                prompts = [
                    [
                        {"role": "system", "content": output["question"]},
                        {"role": "system", "content": output["stage3_prompt"]},
                    ],
                ]
                if faulty_completion:
                    rewards[node_key] += 0.0
                else:
                    final_answer = next(iter(output["final_agent_decision"].items()))[1]
                    completions = [[{"role": "assistant", "content": final_answer}]]
                    cumulative_reward_2(prompts=prompts, completions=completions, **output)
                    rewards[node_key] += sum(node.rewards)

        rewards = sorted(list(rewards.items()), key=lambda x: x[1], reverse=True)
        return [n for n, _ in rewards][:limit]

    return StageData(
        round_winner_fn=round_winners,
        stages=[
            SingleStageData(
                name="0",
                reward_funcs=[
                    stage1_rewards.xmlcount_reward_func,
                    stage1_rewards.soft_format_reward_func,
                    stage1_rewards.strict_format_reward_func,
                    stage1_rewards.int_reward_func,
                    stage1_rewards.correctness_reward_func,
                    cumulative_reward_0,
                ],
                datasets_fn=lambda r, s: (initial_train_dataset, initial_test_dataset),  # type: ignore
            ),
            SingleStageData(
                name="1",
                reward_funcs=[
                    stage2_rewards.proper_id_reward_func,
                    stage2_rewards.correctness_reward_func,
                    stage2_rewards.strict_format_reward_func,
                    stage2_rewards.soft_format_reward_func,
                    stage2_rewards.xmlcount_reward_func,
                    cumulative_reward_1,
                ],
                datasets_fn=stage2_datasets_fn,  # type: ignore
            ),
            SingleStageData(
                name="2",
                reward_funcs=[
                    stage3_rewards.consensus_reward_func,
                    stage3_rewards.concensus_correctness_reward_func,
                    stage3_rewards.question_recreation_reward_func,
                    stage3_rewards.final_correctness_reward_func,
                    stage3_rewards.strict_format_reward_func,
                    stage3_rewards.soft_format_reward_func,
                    stage3_rewards.xmlcount_reward_func,
                    cumulative_reward_2,
                ],
                datasets_fn=stage3_datasets_fn,  # type: ignore
            ),
        ],
    )
