import requests
import json
import time

BASE = "https://aloula.faulio.com/api"

HEADERS = {
    "Origin": "https://www.aloula.sa",
    "Referer": "https://www.aloula.sa/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

M3U_FILE = "saudi.m3u"
JSON_FILE = "saudi.json"


def get_channels():
    url = f"{BASE}/v1/channels"
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return r.json()


def get_stream(channel_id):

    try:
        url = f"{BASE}/v1.1/channels/{channel_id}/player"
        r = requests.get(url, headers=HEADERS, timeout=20)
        data = r.json()

        return data.get("streams", {}).get("hls")

    except:
        return None


def get_logo(ch):

    base = "https://aloula.faulio.com"

    for key in ["image", "thumbnail", "logo"]:
        val = ch.get(key)

        if isinstance(val, str) and val.startswith("/"):
            return base + val

        if isinstance(val, dict):
            path = val.get("path")
            if path:
                return base + path

    return ""


def build_playlist():

    channels = get_channels()

    m3u = "#EXTM3U\n"
    json_data = []

    for ch in channels:

        cid = ch.get("id")
        name = ch.get("title") or ch.get("name")
        logo = get_logo(ch)

        stream = get_stream(cid)

        if stream:

            m3u += f'#EXTINF:-1 tvg-id="{cid}" tvg-logo="{logo}" group-title="Saudi",{name}\n'
            m3u += "#EXTVLCOPT:http-origin=https://www.aloula.sa\n"
            m3u += "#EXTVLCOPT:http-referrer=https://www.aloula.sa/\n"
            m3u += "#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)\n"
            m3u += f"{stream}\n\n"

            json_data.append({
                "id": cid,
                "name": name,
                "logo": logo,
                "stream": stream
            })

            print("✔", name)

        else:
            print("✖", name)

        time.sleep(1)

    with open(M3U_FILE, "w", encoding="utf-8") as f:
        f.write(m3u)

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2)

    print("Playlist updated")


if __name__ == "__main__":
    build_playlist()
