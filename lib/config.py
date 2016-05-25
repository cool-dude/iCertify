import os
import sys
import ConfigParser
from lib import APP_DIR

DEFAULT_CONFIG_NAME = 'data/config.cfg'


def write_sample_config():
    config = ConfigParser.RawConfigParser()
    # When adding sections or items, add them in the reverse order of
    # how you want them to be displayed in the actual file.
    # In addition, please note that using RawConfigParser's and the raw
    # mode of ConfigParser's respective set functions, you can assign
    # non-string values to keys internally, but will receive an error
    # when attempting to write to a file or when you get it in non-raw
    # mode. SafeConfigParser does not allow such assignments to take place.
    config.add_section('app-settings')
    config.set('app-settings', 'font-family', 'fonts/Verdana.ttf')
    config.set('app-settings', 'font-size', 22)
    config.set('app-settings', 'font-colour', (255, 255, 255))
    config.set('app-settings', 'output_format', 'PDF')
    config.set('app-settings', 'attachments', 'attachments')
    config.add_section('user-settings')
    config.set('user-settings', 'xy_cordinates', (100, 50))
    config.set('user-settings', 'certificate', 'data/certificate.jpg')
    config.set('user-settings', 'send_email', True)
    config.add_section('email-sender')
    config.set('email-sender', 'email', 'xxx@gmail.com')
    config.set('email-sender', 'password', 'xyz')
    config.set('email-sender', 'port', 587)
    config.set('email-sender', 'pop_forwarding', 'smtp.gmail.com')

    # Writing our configuration file to 'app.cfg'
    with open(os.path.join(APP_DIR, DEFAULT_CONFIG_NAME), 'wb') as configfile:
        config.write(configfile)


def read_app_config(config_file=os.path.join(APP_DIR, DEFAULT_CONFIG_NAME)):
    if not os.path.exists(config_file):
        sys.stdout.write("Writing a new config since the app doesn't find anyone existing\n")
    write_sample_config()
    config = ConfigParser.RawConfigParser()
    config.read(config_file)
    return config

config = read_app_config()
