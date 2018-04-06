from enum import Enum


class Protocols(Enum):
    HTTP = 'http',
    HTTPS = 'https'


class LocalConst:
    ALEXA_APPLICATION_ID = '<your-alexa-skill-id>'
    LISTEN_KEY = '<your-listen-key>'
    CHANNELS_XML = 'channels.xml'  # Path to your favourite channels file
    PRIVATE_KEY = '<path-to-your-private-key>'  # You will only need this if you use HTTPS if PROTOCOL is HTTPS
    CERTIFICATE = '<path-to-your-certificate>'
    PORT = 5000  # You will probably want 443 if PROTOCOL is HTTPS
    INTERNAL_IP = '<your-local-ip>'  # 0.0.0.0 to listen in all your interfaces.
    URL = '<your-domain>/di_python'  # www.yourdomain.com
    PROTOCOL = Protocols.HTTP

