<h2 align=center>Gensyn Testnet Node Guide</h2>

## 💻 System Requirements

| Requirement                         | Details                                                     |
|-------------------------------------|-------------------------------------------------------------|
| **CPU Architecture**                | `arm64` or `amd64`                                          |
| **Recommended RAM**                 | 24 GB                                                       |
| **CUDA Devices (Recommended)**      | `RTX 3090`, `RTX 4070`, `RTX 4090`, `A100`, `H100`          |
| **Python Version**                  | Python >= 3.10 (For Mac, you may need to upgrade)           |


# Gensyn Protocol

![Gensyn Logo](https://gensyn.ai/images/logo.png)



⚠️ Please read before continuing ⚠️

This software is experimental and provided as-is for users who are interested in using (or helping to develop) an early version of the Gensyn Protocol for training models.

If you care about on-chain participation, you must read the Identity Management section below.

If you encounter issues, please first check Troubleshooting. If you cannot find a solution, check for an open (or closed) Issue. If no relevant issue exists, file a new one and include:





All relevant logs



Information about your device (e.g., GPU, if applicable)



Your operating system details



Table of Contents





Instructions





Run the Swarm



Testnet Participation



Login



Huggingface Integration



Initial Peering and Training



Identity Management





Introduction



Troubleshooting



Contributing



License



Instructions

Run the Swarm

To start the swarm, run the following commands:

python3 -m venv .venv
source .venv/bin/activate
./run_rl_swarm.sh

Testnet Participation

When prompted, answer Y (or press Enter). The N option is provided as an alternative flow but is not currently maintained.

Login





A browser window will open. If you're on a virtual machine, manually navigate to http://localhost:3000/.



Click Login.



Sign in using your preferred method.

Huggingface Integration

Optionally, link your Huggingface account using your HF token. For details, see Huggingface Security Tokens.

Initial Peering and Training

Your device will now contribute to training a hyperscale machine learning system. You should see your peer register and vote on-chain at this address.



Identity Management

Introduction

On-chain identity is managed via an Alchemy modal sign-in screen. You need to provide an email address or log in via a supported method (e.g., Google). This creates an EOA public/private key pair (stored by Alchemy). You will also receive local session keys in userApiKey. Note: These are not your EOA public/private keys.

During initial setup, a swarm.pem file is created to maintain your peer's identity. This is registered on-chain using the EOA wallet hosted in Alchemy, triggered by your local API keys. This links your email address (and corresponding EOA in Alchemy) with swarm.pem permanently. Losing either renders both unusable.

Important for Multi-Node Users: If running multiple nodes and tracking on-chain progress, register each node separately. Do not reuse or copy swarm.pem, userApiKey, userData.json, or email address across nodes. Doing so will prevent on-chain progress tracking. Your node will still train in the swarm, but this will not be reflected on-chain.

Note: If you are using a fork of this repository or a third-party hosted service (e.g., a "one-click" provider), the identity management process is not guaranteed.



Troubleshooting

If you encounter issues:





Review the Troubleshooting section.



Check for existing Issues.



If no solution is found, create a new issue with:





Relevant logs



Device details (e.g., GPU)



Operating system information



Contributing

We welcome contributions! Please read our Contributing Guide for details on how to submit issues, feature requests, or pull requests.



License

This project is licensed under the MIT License.



Happy Training! 🚀

For further support, reach out via Issues or join our community on Discord.
