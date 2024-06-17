# Feedy Notification Server

## Description

Feedy Notification Server is a python server implementation of FCM (Flutter Cloud Messaging) for Feedy.

It allows Feedy app to receive daily watering and misting reminder notifications.

Runs on any server with scheduler. (Linux based distros, windows server or else)

## Installation

Install [Python](https://www.python.org/downloads/source/) (version 3.7 at least)

Following commands runs on Debian based distributions (apt for packet manager)

(`apt-get update` if old references 😉)

`apt-get install python3-pip`

For some reasons, some dependencies were not installed for me 🙄 : `apt-get install libffi6 libffi-dev`

And some needed tools are missing and can be found only with first version of **pip**. Temporary install pip with pip3, you can remove it after if you want.

```
pip3 install --upgrade pip
pip install --upgrade setuptools
pip install --upgrade pyopenssl
```

Finnaly, install firebase for server

`pip3 install firebase-admin`

From your Firebase console, download your service account key in order to get authenticated in your program / script.
(Included empty in this project)

## Crontab

Edit your scheduler to run the script every day, or when your want (for debian and 6pm every day):

`0 18 * * * python /home/feedy/fcm_server.py`

This is obviously just an example.
