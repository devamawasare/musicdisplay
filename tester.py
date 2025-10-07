import acrcloud_api

api_return = acrcloud_api.identify_song("test_recording.m4a")
print(api_return)
url = (api_return.get("album"))
if url:
    print (url + "acr.album.coverart")
else:
    print("no Return")