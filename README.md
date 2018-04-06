# alexa-skill-digitally-imported-python
Web server in Python for your Amazon Alexa skill to play radios on Digitally Imported, Classical Radio, Radio Tunes, Jazz Radio and Rock Radio

<!-- TOC -->
- [Alexa DI.FM Skill for Node.js](#alexa-skill-digitally-imported)
	- [Overview](#overview)
	- [Creating your own skill for Alexa](#creating-your-own-skill-for-alexa)
	- [Setup Guide](#setup-guide)
	- [Getting Started](#getting-started)
	- [Tips](#tips)
<!-- /TOC -->

## Overview


## Creating your own skill for Alexa
If you don't know how to do this, take a look at [Creating your own skill for Alexa](https://github.com/ricardojover/alexa-skill-digitally-imported#creating-your-own-skill-for-alexa)


## Setup Guide
1. Clone the repo
```
https://github.com/ricardojover/alexa-skill-digitally-imported-python.git
```
2. Go to the repo and install dependencies
```
cd alexa-skill-digitally-imported-python.git
pip install Flask
pip install Flask-ask
pip install requests
```
3. Add your favourite channels to the file channels.xml
4. Customize the config file with your own settings.
5. Start the server
```
python server.py
```

If you find the following error:
```
AttributeError: 'module' object has no attribute 'X509V3_EXT_get'
```

You will need to downgrade the cryptography package as follows
```
sudo pip install -U cryptography==2.1.4
```


## Getting Started


## Tips

