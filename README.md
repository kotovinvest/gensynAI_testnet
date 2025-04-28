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



## ⚠️ Пожалуйста, прочитайте перед продолжением ⚠️ / ⚠️ Please read before continuing ⚠️

Это ПО **экспериментальное** и предоставляется как есть для пользователей, заинтересованных в использовании (или помощи в разработке) ранней версии протокола Gensyn для обучения моделей.

This software is **experimental** and provided as-is for users who are interested in using (or helping to develop) an early version of the Gensyn Protocol for training models.

Если для вас важно участие на блокчейне, вы **должны** прочитать раздел [Управление идентичностью](#identity-management) ниже.

If you care a lot about on-chain participation, you **must** read the [Identity Management](#identity-management) section below.

Если вы столкнулись с проблемами, сначала проверьте [Устранение неполадок](#troubleshooting). Если вы не можете найти решение, проверьте, есть ли открытый (или закрытый) [Issue](../../issues). Если нет подходящей проблемы, создайте новую и укажите 1) все соответствующие логи, 2) информацию о вашем устройстве (например, какой GPU, если это применимо), и 3) информацию о вашей операционной системе.

If you encounter issues, please first check [Troubleshooting](#troubleshooting). If you cannot find a solution there, please check if there is an open (or closed) [Issue](../../issues). If there is no relevant issue, please file one and include 1) all relevant logs, 2) information about your device (e.g. which GPU, if relevant), and 3) your operating system information.

## Инструкции / Instructions

## Запуск  / Run the swarm


```sh
python3 -m venv .venv
source .venv/bin/activate
./run_rl_swarm.sh


## Участие в тестовой сети / Testnet participation

Пожалуйста, ответьте 'Y' (или просто нажмите enter), N предоставлен как альтернативный поток, но в настоящее время не поддерживается.

Please answer 'Y' (or just press enter), N is provided as an alternative flow but isn't currently maintained.

## Вход / Login

1. Откроется окно браузера (вам нужно будет вручную перейти по адресу http://localhost:3000/, если вы находитесь в виртуальной машине).
2. Нажмите 'login'.
3. Войдите с использованием предпочитаемого метода.

1. A browser window will pop open (you'll need to manually navigate to http://localhost:3000/ if you're on a VM).
2. Click 'login'.
3. Login with your preferred method.

## Huggingface

По желанию можно связать ваш аккаунт HF с помощью вашего HF токена - [подробности здесь](https://huggingface.co/docs/hub/en/security-tokens).

Optionally pair your HF account by using your HF token - [more here](https://huggingface.co/docs/hub/en/security-tokens).

## Первичное соединение и обучение / Initial peering and training

С этого момента ваше устройство будет использоваться для обучения гипермасштабируемой системы машинного обучения. Вы должны увидеть регистрацию вашего пира и голосование на блокчейне [здесь](https://gensyn-testnet.explorer.alchemy.com/address/0x2fC68a233EF9E9509f034DD551FF90A79a0B8F82?tab=logs).

From this stage onward your device will be used to train a hyperscale machine learning system. You should see your peer register and vote on-chain [here](https://gensyn-testnet.explorer.alchemy.com/address/0x2fC68a233EF9E9509f034DD551FF90A79a0B8F82?tab=logs).

## Управление идентичностью / Identity management

## Введение / Introduction

Идентичность на блокчейне управляется через экран входа Alchemy. Вам нужно указать адрес электронной почты или войти через поддерживаемый метод (например, Google). Это создает публичный/приватный ключ EOA (которые хранятся в Alchemy). Вы также получите локальные ключи сессии в `userApiKey`. Обратите внимание, что это не ваши публичные/приватные ключи EOA.

On-chain identity is managed via an Alchemy modal sign-in screen. You need to supply an email address or login via a supported method (e.g. Google). This creates an EOA public/private key (which are stored by Alchemy). You will also receive local session keys in the `userApiKey`. Note that these aren't your EOA public/private keys.

Во время первоначальной настройки также будет создан файл `swarm.pem`, который поддерживает идентичность вашего пира. Это регистрируется на блокчейне с использованием EOA-кошелька, хранимого в Alchemy, и привязывается с использованием ваших локальных API-ключей. Это связывает `email address` (и соответствующий EOA в Alchemy) + `swarm.pem` навсегда, и они оба фактически теряются, если один из них потерян.

During the initial set-up process, you will also create a `swarm.pem` file which maintains the identity of your peer. This is then registered on-chain using the EOA wallet hosted in Alchemy, triggered using your local API keys. This links the `email address` (and corresponding EOA in Alchemy) + `swarm.pem` forever and they are both effectively burned if one is lost.

Если вы запускаете несколько узлов и хотите отслеживать прогресс на блокчейне (т.е. не только запускать RL Swarm и обучать модель), вам нужно зарегистрироваться снова для каждого узла - не используйте один и тот же `swarm.pem`, `userApiKey`, `userData.json`, `email address` или копируйте данные между узлами. Если вы так сделаете, ваш прогресс не будет отслеживаться на блокчейне. Если вы сделаете одно из этих действий, ваш узел будет работать нормально и обучаться в рое, однако это не будет отражено на блокчейне.

If you are running multiple nodes, and want to track progress on-chain (i.e. not just run RL Swarm itself and train a model), you must sign up again for each node - do not use the same `swarm.pem`, `userApiKey`, `userData.json`, `email address`, or copy the data between the nodes. If you do so, your progress won't be tracked on-chain. If you do any of these things, your node will work fine and train from the swarm however, but this will not be reflected on chain.

**Пожалуйста, обратите внимание**: если вы используете форк этого репозитория или сервис, организованный кем-то другим (например, поставщик "одного клика"), процесс управления идентичностью ниже не гарантирован.

**Please note**: if you are using a fork of this repo, or a service organised by someone else (e.g. a 'one click deployment' provider) the identity management flow below is not guaranteed.
