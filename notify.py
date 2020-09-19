import glib
import dbus
import db_connect
import main
from dbus.mainloop.glib import DBusGMainLoop

# `dbus-send --print-reply --session --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlayPause` -> Send testing signals to 'play & pause' Spotify
# `dbus-monitor --session interface='org.freedesktop.DBus.Properties'` -> Monitoring signals, we can see 'play & pause'

def notifications(bus, message):
    for arg in message.get_args_list():
        if str(arg) == "Spotify":
            db_connect.insert()
            main.notify()
            #print('%s %s \n' % ('arg: ', arg))

DBusGMainLoop(set_as_default=True)
mybus = dbus.SessionBus()
mybus.add_match_string_non_blocking("eavesdrop=true, interface='org.freedesktop.Notifications', member='Notify'")
mybus.add_message_filter(notifications)

myloop = glib.MainLoop()
myloop.run()
