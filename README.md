# RL Swarm

RL Swarm is an open source system for peer-to-peer reinforcement learning over the internet. Running a swarm node allows you to train your personal model against the swarm intelligence. Each swarm performs RL reasoning as a group, with a gossiping system (Hivemind) for collaborative improvement between models. You can also connect your node to the Gensyn Testnet, to receive an on-chain identity that tracks your progress over time.

RL Swarm is fully open and permissionless, meaning you can run it on a basic consumer laptop at home or on a powerful GPU in the cloud. You can also experiment with different models to see which ones perform best.

## Requirements

Ensure that you are using a supported machine/device/environment:

- arm64 or x86 CPU with minimum 16gb ram (note that if you run other applications during training it might crash training).

OR

- CUDA devices (officially supported):
    - RTX 3090
    - RTX 4070
    - RTX 4090
    - A100
    - H100

WITH

-  Python >=3.10 (for Mac, you will likely need to upgrade)

## ⚠️ Please read before continuing ⚠️

This software is **experimental** and provided as-is for users who are interested in using (or helping to develop) an early version of the Gensyn Protocol for training models.

If you care a lot about on-chain participation, you **must** read the [Identity Management](#identity-management) section below.

If you encounter issues, please first check [Troubleshooting](#troubleshooting). If you cannot find a solution there, please check if there is an open (or closed) [Issue](../../issues). If there is no relevant issue, please file one and include 1) all relevant logs, 2) information about your device (e.g. which GPU, if relevant), and 3) your operating system information.

## Instructions

### Run the swarm

```sh
python3 -m venv .venv
source .venv/bin/activate
./run_rl_swarm.sh
```

### Testnet participation

Please answer 'Y' (or just press enter), N is provided as an alternative flow but isn't currently maintained.


### Login

1. A browser window will pop open (you'll need to manually navigate to http://localhost:3000/ if you're on a VM).
2. Click 'login'.
3. Login with your preferred method.

### Huggingface

Optionally pair your HF account by using your HF token - [more here](https://huggingface.co/docs/hub/en/security-tokens).

### Initial peering and training

From this stage onward your device will be used to train a hyperscale machine learning system. You should see your peer register and vote on-chain [here](https://gensyn-testnet.explorer.alchemy.com/address/0x2fC68a233EF9E9509f034DD551FF90A79a0B8F82?tab=logs).


## Identity management

### Introduction

On-chain identity is managed via an Alchemy modal sign-in screen. You need to supply an email address or login via a supported method (e.g. Google). This creates an EOA public/private key (which are stored by Alchemy). You will also receive local session keys in the `userApiKey`. Note that these aren't your EOA public/private keys. 

During the initial set-up process, you will also create a `swarm.pem` file which maintains the identity of your peer. This is then registered on chain using the EOA wallet hosted in Alchemy, triggered using your local api keys. This links the `email address` (and corresponding EOA in Alchemy) + `swarm.pem` forever and they are both effectively burned if one is lost.

If you are running multiple nodes, and want to track progress on-chain (i.e. not just run RL Swarm itself and train a model), you must sign up again for each node - do not use the same `swarm.pem`, `userApiKey`, `userData.json`, `email address`, or copy the data between the nodes. If you do so, your progress won't be tracked on-chain. If you do any of these things, your node will work fine and train from the swarm however, but this will not be reflected on chain.

**Please note**: if you are using a fork of this repo, or a service organised by someone else (e.g. a 'one click deployment' provider) the identity management flow below is not guaranteed.

### What this means
In the following two scenarios, everything will work (i.e. you will have an on-chain identity linked with your RL Swarm peer training):

- The very first time you run the node from scratch with a new email address. The smart account will be created fresh and linked with the swarm.pem that is also fresh.
- If you run it again with a `swarm.pem` AND login the original `email address` used with that `swarm.pem`. Note: this will throw an error into the log on registration but will still be able to sign transactions.

In the following two scenarios, it will not work (i.e. you won't have an on-chain identity linked with your RL Swarm peer training):

- If you lose your original `swarm.pem` and create another one but try to link it to a previously used `email address`.
- If you keep your `swarm.pem` and try to link it to an `email address` distinct from the one with which it was first registered.

Therefore, you should do these actions in the following scenarios

- **Signed up with `email address`, generated `swarm.pem`, BUT lost `swarm.pem`**: run from scratch again with a new email address (you can use the `gmail +` notation for this).
- **Signed up with `email address`, generated `swarm.pem`, kept `swarm.pem`** -> you can re-run a single node using this pair if you've still got them both but not multiple.
- **You want to run multiple nodes at once**: run them all from scratch with different email addresses and generate new `swarm.pem`s for them all (i.e. do not share email address or `swarm.pem` between different running instances).

## Troubleshooting

- **My peer 'skipped a round'**: this occurs when your device isn't fast enough to keep up with the pace of the swarm. For example, if you start training at round 100 and by the time you finish training the rest of the swarm reaches round 102, you will skip round 101 and go straight to 102. This is because your peer is more valuable if it is participating in the active round.
- **My model doesn't seem to be training?**

    - If you're using a consumer device (e.g. a MacBook), it is likely just running slowly - check back in 20 minutes.

- **Logging in with a new account after previous login?**
    
    - Make sure you click 'Logout' on the login screen before you leave your previous session
    - Make sure you delete `swarm.pem` from the root directory (try `sudo rm swarm.pem`). If you don't do this, and you previously registered with the peer-id stored in this file, it will disrupt the training process.

- **Issues with the Login screen**

    - **Upgrade viem**: some users report issues with the `viem` package. There are two fixes:
        - in the `modal-login/package.json` update: `"viem": "2.25.0"`
        - in the terminal `cd /root/rl-swarm/modal-login/ && yarn upgrade && yarn add next@latest && yarn add viem@latest`

- **I'm getting lots of warnings**
    - This is expected behaviour and usually the output of the package managers or other dependencies. The most common is the below Protobuf warning - which can be ignored
        ```
        WARNING: The candidate selected for download or install is a yanked version: 'protobuf' candidate...
        ```

- **Issues on VMs/VPSs?**

    - **How do I access the login screen if I'm running in a VM?**: port forwarding. Add this SSH flag: `-L 3000:localhost:3000` when connecting to your VM. E.g. `gcloud compute ssh --zone "us-central1-a" [your-vm] --project [your-project] -- -L 3000:localhost:3000`. Note, some VPSs may not work with `rl-swarm`. Check the Gensyn [discord](https://discord.gg/zAJbCTk9) for up-to-date information on this.
    
    - **Disconnection/general issues**: If you are tunneling to a VM and suffer a broken pipe, you will likely encounter OOM or unexepected behaviour the first time you relaunch the script. If you `control + c` and kill the script it should spin down all background processes. Restart the script and everything should work normally.

- **Issues with npm/general installation?**

    - Try  `npm install -g node@latest`

- **OOM errors on MacBook?**
    - Try this (experimental) fix to increase memory:
        ```
        export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0
        ```
- **I have a Windows machine, can I still train a model on the swarm?**: Yes - but this is not very well tested and may require you to do some debugging to get it set up properly. Install WSL and Linux on your Windows machine using the following instructions: https://learn.microsoft.com/en-us/windows/wsl/install

- **I want to move my to a different machine and/or restart with a fresh build of the repo, but I want my animal name/peer id to persist.**: To achieve this simply backup the `swarm.pem` file on your current machine and then put it in the corresponding location on your new machine/build of the repo.

- **I have multiple GPUs on one machine, can I run multiple peers?**: Yes - but you'll need to manually change things. You'll need to isolate each GPU, install this repo for each GPU, and expose each peer under a different port to pass the modal onboard.

- **My round/stage is behind the smart contract/other peers?**: This is expected behaviour given the different speeds of machines in the network. Once your machine completes it's current round, it will move to the the current round.

- **I want to use a bigger and/or different model in the RL swarm, can I do that?**: Yes - but we only recommend doing so if you are comfortable manually changing files and appropriately configuring the model(s) you wish to run for your device(s). You'll simply need to edit the config file in `./hivemind_exp/configs/<directory_relevant_to_your_device>/grpo-qwen-2.5-0.5b-deepseek-r1.yaml` to reflect the model_name_or_path and training arguments corresponding to what you want in the swarm. Note that, although any pre-trained LLM compatible with Hugging Face's `AutoModelForCausalLM` class should work in theory, we have only tested with a handful of Qwen 2.5 instruction-tuned models.

- **I am running a model in the swarm on my CPU, have received a python `RuntimeError`, and my training progress seems to have stopped.**: There are several possible causes for this, but before trying anything please wait long enough to be sure your training actually is frozen and not just slow (e.g., wait longer than a single training iteration has previously taken on your machine). If you're sure training is actually frozen, then some things to try are:
    - Set this (experimental) fix: `export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0 && ./run_rl_swarm.sh`
    - In the config for your device (`./hivemind_exp/configs/<directory_relevant_to_your_device>/grpo-qwen-2.5-0.5b-deepseek-r1.yaml`) add the following training argument: `max_grad_norm=0.5`
    - Use floating point 32 instead of bfloat16 to train your model. This can be changed in the config for your device, i.e. `./hivemind_exp/configs/<directory_relevant_to_your_device>/grpo-qwen-2.5-0.5b-deepseek-r1.yaml`.

- **How can I optimsie `rl-swarm` for my device**? open the `hivemind_exp/configs/gpu/grpo-qwen-2.5-0.5b-deepseek-r1.yaml`. Note that this is for the gpu and not cpu configuration. You can then edit parameters that optimsie the training run. For example, try adjusting the `vllm_gpu_memory_utilization`. Note that optimal settings will vary by device.

## Swarm UI
To launch the Swarm UI, run `docker-compose up --build` and open `0.0.0.0:8080` in your browser.

See the [web/README](./web/README.md) for more details.