import subprocess
import os
import re


class modifyMetadata:
    def __init__(self, file, ffpath, artist, album, lyrics, path):
        self.file = file
        # os.path.normcase to format properly
        self.path = os.path.normcase(path)
        self.ffpath = os.path.normcase(ffpath)
        self.fileName = self.re_sub(os.path.basename(self.file), r"[^a-zA-Z0-9\s.]+")
        self.lyrics = lyrics
        return self.edit_metadata(artist, album)

    def re_sub(self, string, rePattern):
        if string == None or string == "":
            return "Uknown"
        newstring = ""
        for i in string:
            newstring += re.sub(rePattern, "", i)
        return newstring

    def edit_metadata(self, artist, album):
        artist = self.re_sub(artist, r"[^a-zA-Z0-9\s.]+")
        album = self.re_sub(album, r"[^a-zA-Z0-9\s.]+")
        # Makes path if it's missing
        if not os.path.exists(self.path + "/" + artist):
            os.mkdir(self.path + "/" + artist)
        if not os.path.exists(self.path + "/" + artist + "/" + album):
            os.mkdir(self.path + "/" + artist + "/" + album)
        path = self.path + "/" + artist + "/" + album + "/" + self.fileName
        # using ffmpeg
        if self.lyrics is not None:
            args = [
                os.path.join(self.ffpath, "ffmpeg"),
                "-i",
                self.file,
                "-metadata",
                "artist=" + artist,
                "-metadata",
                "album=" + album,
                "-metadata",
                "lyrics=" + self.lyrics,
                "-c",
                "copy",
                path,
            ]
        else:
            args = [
                os.path.join(self.ffpath, "ffmpeg"),
                "-i",
                self.file,
                "-metadata",
                "artist=" + artist,
                "-metadata",
                "album=" + album,
                "-c:a",
                "copy",
                path,
            ]
        ffmpeg = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
