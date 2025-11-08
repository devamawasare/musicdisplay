from unittest.util import strclass
from PyQt5.QtCore import QObject, pyqtSignal
from .recognizer import recognize_current_song
from dataclasses import dataclass

import acrcloud_api
import helpers

@dataclass(frozen = True)
class Track:
    title: str
    artist: str | None = None
    album: str | None = None
    cover_url: str | None = None

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
    AUDIO_FILE_PATH = "audio_files/test_recording_2.m4a"

    api_response =  (acrcloud_api.identify_song(AUDIO_FILE_PATH))
    if api_response == None:
        print("API Request Failed")
        return None

    if helpers._get(api_response, ['status', 'code']) != 0:
        print("Song Search Failed")
        return None

    #print (helpers._get(api_response, ['metadata','music',0,'external_metadata']))
    #TODO: Add artist name handling 
    if helpers._get(api_response, ['metadata','music',0,'external_metadata','spotify']) != None:
        track_name = helpers._get(api_response, ['metadata','music',0,'external_metadata','spotify', 'track', 'name'])
        album_name = helpers._get(api_response, ['metadata','music',0,'external_metadata','spotify', 'album', 'name'])
        return Track(title = track_name, album = album_name)
    else:
        print("No Spotify Match")
        return None