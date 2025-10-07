import requests

spotify_album_id = "4m2880jivSbbyEGAKfITCa"

def spotify_oembed(spot_url: str) -> str | None:
    try:
        r = requests.get(
            "https://open.spotify.com/oembed",
            params={"url": spot_url},
            timeout=5,
        )
        if r.ok:
            data = r.json()
            return data.get("thumbnail_url")
    except Exception:
        pass
    return None

thumb = spotify_oembed(f"https://open.spotify.com/album/{spotify_album_id}")

print (thumb)