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
In this application I'm using [Flask-Ask](http://flask-ask.readthedocs.io/en/latest/) which is a "Rapid Alexa Skills Kit Development for Amazon Echo Devices". From my point of view this is by far the quickest way to create your own skills.
But there are more alternatives and you can find them in the official [Alexa GitHub Site](https://github.com/alexa/).


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
This is pretty similar to [Getting Started](https://github.com/ricardojover/alexa-skill-digitally-imported#getting-started) on my other project written in NodeJS.
The main difference is that in this project I've decided to load the favourite channels from a file instead of hardcode them in the code. So you will have to edit the file channels.xml and change it accordingly.


## Tips
* If you already have a web server running in your server with all certificates configured and so on, you can just set the internal IP to 127.0.0.1 and create a reverse proxy. In my case I'm doing this with Nginx.
* Talking about Nginx, if you are not comfortable with the proxy part in Python, you can leave Nginx struggling with it. You will only need to pass the DI url as parameter and create the proxy dinamically.
```python
@app.route('/di_python/<channel_name>')
def di_python(channel_name):
    print "Creating proxy"
    listen_key = request_ask.args.get('listen_key')
    url = get_actual_url(channel_name, listen_key)
    req = requests.get(url, stream=True)
    return Response(stream_with_context(req.iter_content(chunk_size=1024)), content_type=req.headers['content-type'])
```

If you decide to use Nginx, don't forget to set some rules or just deny all traffic not coming from the localhost as creating a proxy like that in your own server could be dangerous.
It could be something like this

```
location /di_python {
	allow 127.0.0.1;
	deny all;
	resolver 8.8.8.8;
	proxy_pass $arg_url;
	proxy_set_header Host $host;
	proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
```

For more tips visit [Tips](https://github.com/ricardojover/alexa-skill-digitally-imported#tips)
