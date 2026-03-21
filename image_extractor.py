import requests


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


def fetch_image_bytes(url: str) -> bytes | None:
    try:
        r = requests.get(url, timeout=5)
        if r.ok:
            return r.content
    except Exception:
        pass
    return None


if __name__ == "__main__":
    spotify_album_id = "4m2880jivSbbyEGAKfITCa"
    thumb = spotify_oembed(f"https://open.spotify.com/album/{spotify_album_id}")
    print(thumb)
