"""
To use this configuration, rename the file
from config_sample.py to config.py
"""

def image_display(url):
    return "data:text/html,<img src='" + url + "' style='width: 100%;position:fixed;top:50%;left:50%;transform: translate(-50%,-50%)' /><script>setTimeout(function(){location.reload()}, 10*60*1000)</script>"

WEATHER_URL = image_display('https://wttr.in/.png?2nF')

def custom_init_response(message):
    config = message['local_config'] if 'local_config' in message else {}
    data = {
        'side_iframes': [],
        # set to True if you only want a person to be able to control their status only on
        # their own board; otherwise, you can control anyone's status you are following.
        'accesscontrol': False
    }

    data['side_iframes'].append({
        'name': 'weather',
        'url': WEATHER_URL,
        'height': '1.5fr'
    })

    # you can add additional side iframes by appending to data['side_iframes'],
    # and also do so conditionally based on query parameters (i.e.,
    # with URL http://statusboard/you/friend?foo&bar=baz, config['foo']
    # would be set to true and config['bar'] would be "baz".

    # One-column mode only shows the current status of each user, and requires you to
    # click in order to change the status to something else. If set, you can use the
    # reclaimed space underneath the status area for a main iframe. For example:

    if 'full_iframe' in config:
        data['onecol'] = True
        data['main_iframe'] = {
            'url': 'http://theoldpurple.com'
        }

    return data


from statuses import Status

# You can set custom statuses in this file.
# To use the defaults, set custom_statuses to None.
custom_statuses = [
    Status("BUSY", "Busy", "#930000"),
    Status("WORKING", "Working", "#c07c00"),
    Status("AVAILABLE", "Available", "#007600", blink=True)
]