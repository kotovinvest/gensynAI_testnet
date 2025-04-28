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



## ⚠️ Please read before continuing ⚠️

This software is **experimental** and provided *as-is* for users who are interested in using (or helping to develop) an early version of the Gensyn Protocol for training models.

If you care about *on-chain participation*, you **must** read the [Identity Management](#identity-management) section below.

If you encounter issues, please first check [Troubleshooting](#troubleshooting). If you cannot find a solution, check for an open (or closed) [Issue](../../issues). If no relevant issue exists, file a new one and include:
1. All relevant logs
2. Information about your device (e.g., GPU, if applicable)
3. Your operating system details

---

## Table of Contents
- [Instructions](#instructions)
  - [Run the Swarm](#run-the-swarm)
  - [Testnet Participation](#testnet-participation)
  - [Login](#login)
  - [Huggingface Integration](#huggingface-integration)
  - [Initial Peering and Training](#initial-peering-and-training)
- [Identity Management](#identity-management)
  - [Introduction](#introduction)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Instructions

### Run the Swarm


To start the swarm, run the following commands:

```sh
python3 -m venv .venv
source .venv/bin/activate
./run_rl_swarm.sh

**Testnet Participation**

Please answer **Y** (or just press Enter), **N** is provided as an alternative flow but isn't currently maintained.

### Login

A browser window will open (you'll need to manually navigate to [http://localhost:3000/](http://localhost:3000/), if you're on a VM).

Click **Login**.

Login with your preferred method.

### Huggingface Integration

Optionally pair your HF account by using your HF token - more here.

### Initial Peering and Training

From this stage onward your device will be used to train a hyperscale machine learning system. You should see your peer register and vote on-chain here.

### Identity Management

#### Introduction

On-chain identity is managed via an Alchemy modal sign-in screen. You need to supply an email address or login via a supported method (e.g., Google). This creates an EOA public/private key (which are stored by Alchemy). You will also receive local session keys in **userApiKey**. Note that these aren't your EOA public/private keys.

During the initial set-up process, you will also create a **swarm.pem** file which maintains the identity of your peer. This is then registered on-chain using the EOA wallet hosted in Alchemy, triggered using your local API keys. This links the email address (and corresponding EOA in Alchemy) + swarm.pem forever and they are both effectively burned if one is lost.

#### Important for Multi-Node Users:

If you are running multiple nodes, and want to track progress on-chain (i.e., not just run RL Swarm itself and train a model), you must sign up again for each node - do not use the same **swarm.pem**, **userApiKey**, **userData.json**, email address, or copy the data between the nodes. If you do so, your progress won't be tracked on-chain. If you do any of these things, your node will work fine and train from the swarm, but this will not be reflected on-chain.

Note: If you are using a fork of this repository or a third-party hosted service (e.g., a "one-click" provider), the identity management process below is not guaranteed.

### Troubleshooting

If you encounter issues:

- Review the **Troubleshooting** section.
- Check for existing Issues.
- If no solution is found, create a new issue with:
  - Relevant logs
  - Device details (e.g., GPU)
  - Operating system information

### Contributing

We welcome contributions! Please read our **Contributing Guide** for details on how to submit issues, feature requests, or pull requests.

### License

This project is licensed under the MIT License.

**Happy Training! 🚀**

For further support, reach out via Issues or join our community on Discord.

## ⚠️ Пожалуйста, прочтите перед продолжением ⚠️

Это ПО является **экспериментальным** и предоставляется *как есть* для пользователей, которые заинтересованы в использовании (или помощи в разработке) ранней версии Протокола Gensyn для обучения моделей.

Если вам важна *участие в цепочке (on-chain)*, вы **должны** прочитать раздел [Управление идентификацией](#identity-management) ниже.

Если у вас возникнут проблемы, сначала проверьте раздел [Поиск решений](#troubleshooting). Если решение не найдено, проверьте открытые (или закрытые) [Issues](../../issues). Если нет подходящей проблемы, создайте новую и включите:
1. Все соответствующие логи
2. Информацию о вашем устройстве (например, GPU, если применимо)
3. Детали вашей операционной системы

---

## Содержание
- [Инструкции](#instructions)
  - [Запуск Swarm](#run-the-swarm)
  - [Участие в тестовой сети](#testnet-participation)
  - [Авторизация](#login)
  - [Интеграция с Huggingface](#huggingface-integration)
  - [Начальная синхронизация и обучение](#initial-peering-and-training)
- [Управление идентификацией](#identity-management)
  - [Введение](#introduction)
- [Поиск решений](#troubleshooting)
- [Участие в проекте](#contributing)
- [Лицензия](#license)

---

## Инструкции

### Запуск Swarm

Чтобы запустить swarm, выполните следующие команды:

```sh
python3 -m venv .venv
source .venv/bin/activate
./run_rl_swarm.sh

**Участие в тестовой сети**

Пожалуйста, ответьте **Y** (или просто нажмите Enter), **N** предоставляется как альтернативный поток, но в настоящее время не поддерживается.

### Авторизация

Откроется окно браузера (если вы используете виртуальную машину, вам нужно будет вручную перейти по адресу [http://localhost:3000/](http://localhost:3000/)).

Нажмите **Login**.

Авторизуйтесь с использованием предпочитаемого метода.

### Интеграция с Huggingface

Опционально привяжите ваш аккаунт HF с использованием вашего HF токена - подробности здесь.

### Начальная синхронизация и обучение

С этого этапа ваше устройство будет использоваться для обучения гипермасштабируемой системы машинного обучения. Вы должны увидеть, как ваш пир регистрируется и голосует в цепочке здесь.

### Управление идентификацией

#### Введение

Идентификация в цепочке управляется через экран авторизации Alchemy. Вам нужно предоставить адрес электронной почты или войти через поддерживаемый метод (например, Google). Это создаст публичный/приватный ключ **EOA** (которые хранятся в Alchemy). Вы также получите локальные ключи сессии в **userApiKey**. Обратите внимание, что это не ваши публичные/приватные ключи **EOA**.

В процессе начальной настройки вы также создадите файл **swarm.pem**, который будет хранить идентичность вашего пира. Этот файл затем регистрируется в цепочке с использованием **EOA** кошелька, размещенного в Alchemy, и запускается с помощью ваших локальных **API ключей**. Это связывает адрес электронной почты (и соответствующий **EOA** в Alchemy) + **swarm.pem** навсегда, и они оба фактически сгорают, если один из них теряется.

#### Важно для пользователей с несколькими узлами:

Если вы запускаете несколько узлов и хотите отслеживать прогресс в цепочке (т.е. не просто запускать RL Swarm и обучать модель), вам нужно снова зарегистрироваться для каждого узла — не используйте одинаковые **swarm.pem**, **userApiKey**, **userData.json**, адрес электронной почты и не копируйте данные между узлами. В противном случае ваш прогресс не будет отслеживаться в цепочке. Если вы сделаете одно из этих действий, ваш узел будет нормально работать и обучать модель из swarm, но это не будет отражено в цепочке.

Примечание: если вы используете форк этого репозитория или стороннюю хостинговую службу (например, "one-click" провайдера), процесс управления идентификацией ниже не гарантирован.

### Поиск решений

Если у вас возникли проблемы:

- Ознакомьтесь с разделом **Поиск решений**.
- Проверьте существующие **Issues**.
- Если решение не найдено, создайте новый **issue** с:
  - Соответствующими логами
  - Информацией об устройстве (например, GPU)
  - Информацией о вашей операционной системе

### Участие в проекте

Мы приветствуем вклад! Пожалуйста, ознакомьтесь с нашим **Руководством по внесению вклада** для получения информации о том, как отправлять **issues**, запросы на функции или **pull-запросы**.

### Лицензия

Этот проект лицензирован под лицензией **MIT**.

**Удачного обучения! 🚀**
