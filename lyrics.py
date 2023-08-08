import urllib.request
import urllib.parse
import urllib.error
import json
import re
import html


class lyrics:
    def __init__(self, key, artist, song):
        self.key = key
        self.Class = "Lyrics__Container-sc-1ynbvzw-5 Dzxov"
        self.artist = artist
        self.song = song

    def getLyrics(self):
        badhtml = self.requestGenius(self.key, self.artist, self.song)
        if badhtml is None:
            return None
        goodhtml = re.findall(
            r"<div data-lyrics-container=\"true\" class=\"Lyrics__Container-sc-1ynbvzw-5 Dzxov\">(.*?)<\/div>",
            badhtml,
            re.DOTALL,
        )
        goodhtml = "\n".join(goodhtml)
        goodhtml = goodhtml.replace("<br/>", "\n")
        goodhtml = html.unescape(goodhtml)
        goodhtml = re.sub(r"<.*?>", "", goodhtml)
        return goodhtml

    def requestGenius(self, key, artist, song):
        base_url = "https://api.genius.com"
        search_path = "/search"
        headers = {"Authorization": "Bearer " + key}
        query = urllib.parse.quote(f"{artist} {song}")
        url = f"{base_url}{search_path}?q={query}"

        req = urllib.request.Request(url, headers=headers)

        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                if "response" in data and "hits" in data["response"]:
                    url = data["response"]["hits"][0]["result"]["url"]
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0"
                    }
                    request = urllib.request.Request(url, headers=headers)

                    response = urllib.request.urlopen(request)

                    html_content = response.read().decode("utf-8")

                    return html_content

                else:
                    return None
        except urllib.error.HTTPError as e:
            print(f"HTTP Error: {e.code} - {e.reason}")
            return None
        except urllib.error.URLError as e:
            print(f"URL Error: {e.reason}")
            return None
