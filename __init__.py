# pynicotine from nicotine+, see https://github.com/nicotine-plus/nicotine-plus/tree/master/pynicotine
from pynicotine.pluginsystem import BasePlugin
from pynicotine.config import config
from pynicotine.external.tinytag import TinyTag
from pynicotine.utils import encode_path
from addMetadata import modifyMetadata
from lyrics import lyrics
import os


configfile = config.get_user_directories()[0]
with open(configfile + "/config") as f:
    for i in f.readlines():
        if i.startswith("downloaddir"):
            # This adds the selected download folder as where to format the songs to
            DEFAULT_DIR = i.split("=")[1].strip()
            break

# If you want to override the default download dir
# DEFAULT_DIR = "D:/Music/"

# Your Genius API key
APIKEY = "API_KEY"
# Folder that has ffmpeg
FFFOLDER = "FFMPEG_PATH"


class Plugin(BasePlugin):
    def __init__(self):
        super().__init__()

    # Modifying the function that is called once the file is finished downloading
    def download_finished_notification(self, user, virtual_path, real_path):
        added = True
        if APIKEY == "API_KEY":
            self.log("Please add your Genius API key to the plugin")
            added = False
        if FFFOLDER == "FFMPEG_PATH":
            self.log("Please add the path to ffmpeg to the plugin")
            added = False
        if not added:
            return
        extension = os.path.splitext(real_path)[1]
        if extension != ".flac" and extension != ".mp3":
            self.log(f"File is at {real_path}, couldn't move file")
            return
        tags = TinyTag()
        tags = tags.get(encode_path(real_path))
        fileArtist, fileTitle, fileAlbum = tags.artist, tags.title, tags.album
        request = lyrics(APIKEY, fileArtist, fileTitle)
        lyric = request.getLyrics()
        modifyMetadata(
            real_path,
            FFFOLDER,
            fileArtist,
            fileAlbum,
            lyric,
            DEFAULT_DIR,
        )
        self.log(f"Lyrics added to {fileTitle}")

    def log(self, *msg):
        super().log(*msg)
