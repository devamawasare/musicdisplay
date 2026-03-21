from PyQt5.QtCore import QObject, pyqtSignal
from dataclasses import dataclass

import acrcloud_api
import helpers
from image_extractor import spotify_oembed, fetch_image_bytes
from audio_capture import record_clip


@dataclass(frozen=True)
class Track:
    title: str
    artist: str | None = None
    album: str | None = None
    cover_bytes: bytes | None = None


class recognizer_worker(QObject):
    trackFound = pyqtSignal(Track)
    nothingFound = pyqtSignal()
    error = pyqtSignal(str)

    def try_recognition(self) -> None:
        try:
            track = recognize_current_song()
            if track:
                self.trackFound.emit(track)
            else:
                self.nothingFound.emit()
        except Exception as e:
            self.error.emit(str(e))


def recognize_current_song() -> Track | None:
    audio_path = record_clip()

    api_response = acrcloud_api.identify_song(audio_path)
    if api_response is None:
        print("API Request Failed")
        return None

    if helpers._get(api_response, ['status', 'code']) != 0:
        print("Song Search Failed")
        return None

    # Try Spotify metadata first
    if helpers._get(api_response, ['metadata', 'music', 0, 'external_metadata', 'spotify']) is not None:
        track_name = helpers._get(api_response, ['metadata', 'music', 0, 'external_metadata', 'spotify', 'track', 'name'])
        album_name = helpers._get(api_response, ['metadata', 'music', 0, 'external_metadata', 'spotify', 'album', 'name'])
        artist_name = helpers._get(api_response, ['metadata', 'music', 0, 'external_metadata', 'spotify', 'artists', 0, 'name'])
        album_id = helpers._get(api_response, ['metadata', 'music', 0, 'external_metadata', 'spotify', 'album', 'id'])

        cover_bytes = None
        if album_id:
            thumb_url = spotify_oembed(f"https://open.spotify.com/album/{album_id}")
            if thumb_url:
                cover_bytes = fetch_image_bytes(thumb_url)

        return Track(title=track_name, artist=artist_name, album=album_name, cover_bytes=cover_bytes)

    # Fallback to native ACRCloud fields
    track_name = helpers._get(api_response, ['metadata', 'music', 0, 'title'])
    artist_name = helpers._get(api_response, ['metadata', 'music', 0, 'artists', 0, 'name'])
    if track_name:
        return Track(title=track_name, artist=artist_name)

    print("No Match Found")
    return None
