import re
import requests
from flask import Flask, request as request_ask, Response, stream_with_context
from flask_ask import (
    Ask,
    audio,
    statement,
    question,
)
from config import Protocols, LocalConst
from di_fm import Favourites

app = Flask(__name__)
app.config['ASK_APPLICATION_ID'] = LocalConst.ALEXA_APPLICATION_ID
ask = Ask(app, "/alexa-di-fm-python")
di_favourites = Favourites()


def validate_actual_url(url):
    print "Validating URL: '{0}'".format(url)
    res = requests.head(url)
    return res


@app.route('/di_python/<channel_name>')
def di_python(channel_name):
    print "Creating proxy"
    listen_key = request_ask.args.get('listen_key')
    url = get_actual_url(channel_name, listen_key)
    req = requests.get(url, stream=True)
    return Response(stream_with_context(req.iter_content(chunk_size=1024)), content_type=req.headers['content-type'])


def play_channel(channel_name):
    my_channels = di_favourites.get_channels()
    channel_object = my_channels[channel_name]
    card_tile = channel_object.site
    card_body = channel_object.title
    card_small_image = channel_object.small_image_url
    card_large_image = channel_object.large_image_url
    message = "Playing " + channel_object.title
    print message
    url = get_secure_url(channel_name, LocalConst.LISTEN_KEY)
    return audio(message).play(url).standard_card(title=card_tile, text=card_body,
                                                  small_image_url=card_small_image,
                                                  large_image_url=card_large_image)


def play(channel_name):
    print "Found slot name '{0}'".format(channel_name)
    my_channels = di_favourites.get_channels()

    if channel_name not in my_channels:
        print "Requested channel '{0}' not found".format(channel_name)
        if channel_name is not None:
            not_valid = "The channel '{0}' is not a valid channel.".format(channel_name)
        else:
            not_valid = "I'm sorry, I didn't understand."

        q = not_valid + " What channel do you want to play ?"

        print "Waiting for user response after invalid channel '{0}'".format(channel_name)
        return question(q).reprompt("The valid channels are " + di_favourites.to_string())

    ready_to_play, message = try_play_channel(channel_name)
    if not ready_to_play:
        return audio(message).stop()

    return play_channel(channel_name)


def try_play_channel(channel_name):
    url = get_actual_url(channel_name, LocalConst.LISTEN_KEY)
    res = validate_actual_url(url)
    print "Status Code: '{0}'".format(res.status_code)
    if res.status_code == requests.codes.ok:
        ready_to_play = True
        message = "OK"
    else:
        ready_to_play = False
        if res.status_code == requests.codes.not_found:
            message = "Digital imported does not have a '{0}' channel".format(channel_name)
        elif res.status_code == requests.codes.unauthorized:
            message = "The listen key you are using is not valid"
        else:
            message = "The web site has return the code '{0}'".format(str(res.status_code))

    return ready_to_play,message


def get_actual_url(channel_name, listen_key):
    my_channels = di_favourites.get_channels()
    channel_object = my_channels[channel_name]
    url = channel_object.baseUrl + channel_name.lower() + channel_object.suffix + '?' + listen_key

    return url


def get_secure_url(channel_name, listen_key):
    channel_name = re.sub(r"\s+", "", channel_name)
    url = "https://{0}/{1}?listen_key={2}".format(LocalConst.URL, channel_name, listen_key)
    return url


@ask.launch
def start_skill():
    welcome_message = "Tell Digitally Imported what channel you want to play"
    return question(welcome_message)


@ask.intent("PlayIntent")
@ask.intent("AMAZON.ResumeIntent")
def play_audio(Channel):  # Channel is the name of our Intent Slot
    if not Channel:
        return unhandled()
    return play(Channel)


@ask.intent("AMAZON.StopIntent")
@ask.intent("AMAZON.PauseIntent")
@ask.intent("AMAZON.CancelIntent")
def stop_audio():
    bye_text = 'Ok, stopping music... bye'
    return audio(bye_text).stop()


@ask.intent("Unhandled")
def unhandled():
    text = "I couldn't understand. Please, try again"
    return statement(text)


if __name__ == '__main__':
    if LocalConst.PROTOCOL == Protocols.HTTPS:
        context = (LocalConst.CERTIFICATE, LocalConst.PRIVATE_KEY)
    else:
        context = None

    app.run(host=LocalConst.INTERNAL_IP, port=LocalConst.PORT, debug=False,
            threaded=True, ssl_context=context)
