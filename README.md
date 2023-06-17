# discord-planning-bot
A discord bot that can create date ranges to help plan future events

## Installing requirements on EC2

Upgrade `apt`
```shell
sudo apt-get update && sudo apt-get upgrade -y
```

Upgrade `pip`
```shell
/usr/bin/python3 -m pip install --upgrade pip
```

Install Requirements
```shell
cd discord-planning-bot
pip install -r ./requirements.txt
```

Run App
```shell
python3 main.py
```

## Local Testing

1. Place AWS access keys in `~/.aws`
2. `local.cnf` entry for AWS profile indicates which credentials will be used:
```
[aws]
profile_name=default
```
Note: `local.cnf` should **not** be deployed snce production does not use AWS credentials for auth.

