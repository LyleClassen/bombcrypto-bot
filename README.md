# bombcrypto-bot

A bot to automate the bombcrypto game.

This bot supports multiple accounts open on the same screen, and use of multiple worspaces.

## How to install

Install requirements:
```shell
pip install -r requirements.txt
```

### Multiple worspaces

For the multi-workspace system to work, install the following libraries on your operating system.

#### Windows

Install [PSVirtualDesktop](https://github.com/MScholtes/PSVirtualDesktop):
```shell
PS C:\> Install-Module VirtualDesktop
```

#### Linux

Install wmctrl:
```shell
sudo apt-get install -y wmctrl
```

## Usage

Run the bot:
```shell
python -m bot
```

## Settings

Bot settings are stored in the `settings.yaml` file. You can edit this file to change the bot's behavior.

## Donate

This bot is free to use, but if you like it, please consider donating to the creator.

BSC wallet: `0xBF2071C76b96D1396531D343651ea2154fF7c5A5`