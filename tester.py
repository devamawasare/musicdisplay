import acrcloud_api
import helpers
import sys

AUDIO_FILE_PATH = "audio_files/test_recording_2.m4a"

api_response =  (acrcloud_api.identify_song(AUDIO_FILE_PATH))
if api_response == None:
    print("API Request Failed")
    sys.exit(1)

if helpers._get(api_response, ['status', 'code']) != 0:
    print("Song Search Failed")
    sys.exit(1)

#print (helpers._get(api_response, ['metadata','music',0,'external_metadata']))

if helpers._get(api_response, ['metadata','music',0,'external_metadata','spotify']) != None:
    track_name = helpers._get(api_response, ['metadata','music',0,'external_metadata','spotify', 'track', 'name'])
    album_name = helpers._get(api_response, ['metadata','music',0,'external_metadata','spotify', 'album', 'name'])
    print (f'{track_name} - {album_name}')
else:
    print("No Spotify Match")
