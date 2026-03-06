import requests
import json
import time

BASE = "https://aloula.faulio.com/api"
HEADERS = {
    "Origin": "https://www.aloula.sa",
    "User-Agent": "Mozilla/5.0"
}

M3U_FILE = "saudi.m3u"
JSON_FILE = "saudi.json"

# headers required by the stream server
STREAM_HEADERS = "Origin=https://www.aloula.sa&Referer=https://www.aloula.sa/&User-Agent=Mozilla/5.0"


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


def build_playlist():
    channels = get_channels()

    m3u = "#EXTM3U\n"
    json_data = []

    for ch in channels:

        cid = ch.get("id")
        name = ch.get("title") or ch.get("name")

        logo = ""
        if ch.get("image"):
            logo = "https://aloula.faulio.com" + ch["image"]

        stream = get_stream(cid)

        if stream:

            # add required headers to stream
            stream_with_headers = f"{stream}|{STREAM_HEADERS}"

            m3u += f'#EXTINF:-1 tvg-id="{cid}" tvg-logo="{logo}" group-title="Saudi",{name}\n'
            m3u += f"{stream_with_headers}\n\n"

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
