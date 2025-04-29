import sys
import urllib.parse
import xbmcplugin
import xbmcgui
import xbmcaddon
from resources.lib import sdilej

addon = xbmcaddon.Addon()
USERNAME = addon.getSetting("sdilej_user")
PASSWORD = addon.getSetting("sdilej_pass")

handle = int(sys.argv[1])
args = dict(urllib.parse.parse_qsl(sys.argv[2][1:]))

def list_movies():
    movies = [
        {
            "title": "Minecraft Film (2025)",
            "url": "https://www.sdilej.cz/30973795/minecraft-film-cz-dabing-2025-topkvalita.mp4"
        }
    ]
    for movie in movies:
        li = xbmcgui.ListItem(label=movie['title'])
        li.setInfo(type="Video", infoLabels={"title": movie['title']})
        li.setProperty("IsPlayable", "true")
        url = f"{sys.argv[0]}?action=play&url={urllib.parse.quote_plus(movie['url'])}"
        xbmcplugin.addDirectoryItem(handle, url, li, False)
    xbmcplugin.endOfDirectory(handle)

def play_video(page_url):
    try:
        from xbmcaddon import Addon
        addon = Addon()
        user = addon.getSetting("sdilej_user")
        pwd = addon.getSetting("sdilej_pass")

        stream_url = sdilej.get_stream_url(page_url, user, pwd)
        li = xbmcgui.ListItem(path=stream_url)
        xbmcplugin.setResolvedUrl(handle, True, li)
    except Exception as e:
        dialog = xbmcgui.Dialog()
        dialog.notification("Chyba", str(e), xbmcgui.NOTIFICATION_ERROR)


def run():
    if args.get("action") == "play":
        play_video(args["url"])
    else:
        list_movies()
