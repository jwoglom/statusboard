# Statusboard
Statusboard lets you create a customizable signage board, where you can mark your availability alongside roommates or friends. It is ideally suited for use on a small touch-screen tablet which you can set near your workspace, so that it can both let you see whether the other people you're tracking are available or busy, and display things like a clock, your calendar, and the weather which you want to be able to see at a glance.

<img src="https://i.imgur.com/Nra1sex.gif" width=800 />


## Setup
A basic setup is quite simple:
1. Run an instance of the statusboard Flask application at an accessible URL. Rename *config_sample.py* to *config.py* to enable the default configuration.
2. Find two tablets which can run a full-screen web browser: Windows 8/10-era tablets or Android devices are ideal. On Windows, disable sleep mode while the device is plugged in. On Android, enable the developer setting to never turn off the display while plugged in.
3. On each tablet, open Chrome or an equivalent web browser to:

   **http://statusboard-host/myusername/followusername**
   
   If you want to follow multiple users, you can specify multiple followers:
   
   **http://statusboard-host/myusername/follower1,follower2**
   
4. You're done! You can configure custom iframe widgets and other settings (such as _accesscontrol_, which restricts you from changing the status of your followers) in config.py. The following screenshot should show the result of setting your own username as *james* and followers as *person1* and *person2*:

<img src="https://i.imgur.com/WL7g2V3.png" width=800 />

### Custom Configuration

<img src="https://i.imgur.com/meGpfSQ.png" width=800 />

Create a file *config.py* with the following:
```python

def custom_init_response(message):
  return {
    'side_iframes': [{
      'name': 'custom_widget1',
      'url': 'http://custom-widget-url',
      'height': '1.5fr'
    }, {
      'name': 'custom_widget2',
      'url': 'http://custom-widget-url',
      'height': '1.5fr'
    }],
    'onecol': True,
    'main_iframe': {
      'name': 'calendar_widget',
      'url': 'http://google-calendar-embed-url',
    },
    'accesscontrol': False
  }
```

The `onecol` setting changes the UI behavior to display only the current status of each user, rather than showing all of the available statuses and highlighting each user's current status. This allows for a `main_iframe` to be set, which takes up the area underneath the status display.

If `accesscontrol` is set, then you will only be able to change your own status, and the statuses of your followers will be read only to you.

### Custom Statuses

You can control the default status names and colors by adding the following to the bottom of *config.py*:
```python
from statuses import Status

# You can set custom statuses in this file.
# To use the defaults, set custom_statuses to None.
custom_statuses = [
    Status("BUSY", "Busy", "#930000"),
    Status("WORKING", "Working", "#c07c00"),
    Status("AVAILABLE", "Available", "#007600", blink=True)
]
```

The custom parameter `blink=True` will cause the background of the status to blink between black and the denoted color.
