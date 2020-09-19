from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import dbus
import notify2
import settings

APP_NAME = "100tipy"
SPOTIFY_CLIENT_ID = settings.SPOTIFY_CLIENT_ID
SPOTIFY_CLIENT_SECRET = settings.SPOTIFY_CLIENT_SECRET

def get_track_info(track_id):
    client_credentials_manager = SpotifyClientCredentials(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    track = spotify.track(track_id)
    title = track.get("name")
    artists = []
    for artist in track.get("artists"):
        artists.append(artist.get("name"))

    album = track.get("album").get("name")
    duration = track.get("duration_ms")

    return title, artists, album, duration

def get_track_id():
    session_bus = dbus.SessionBus()
    spotify_bus = session_bus.get_object("org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2")
    spotify_properties = dbus.Interface(spotify_bus, "org.freedesktop.DBus.Properties")
    metadata = spotify_properties.Get("org.mpris.MediaPlayer2.Player", "Metadata")
    track_id = metadata['mpris:trackid']
    return track_id

def show_notify(notification, title, message):
       notification.update(title, message)
       notification.show()

def notify():
    track_id = get_track_id()
    title, artist, album, duration = get_track_info(track_id)
    notify2.init(APP_NAME)
    notification = notify2.Notification(APP_NAME, None, APP_NAME)
    notification.set_urgency(notify2.URGENCY_NORMAL)
    notification.set_timeout(3000)

    duration = duration / 1000
    minutes = duration / 60
    seconds = duration % 60
    message = '%s - %s (%d:%02d)' % (artist[0], album, minutes, seconds)

    show_notify(notification, title, message)

# TODO: Improve the notifications
