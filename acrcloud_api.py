import time
import base64
import hmac
import hashlib
import requests

#API Credentials

ACCESS_KEY = "8cfb53e806fa2086e4cca3b10044d6d0"
SECRET_KEY = "cvUHQn9PLPMQbx49oFMHOuZ2J3TEEGaiQgcJjOeX"
HOST = "identify-us-west-2.acrcloud.com"

def identify_song (audio_file_path):
    with open(audio_file_path, 'rb') as f:
        sample_bytes = f.read()

    http_method = "POST"
    http_uri = "/v1/identify"
    data_type = "audio"
    signature_version = "1"
    timestamp = str(int(time.time()))

    string_to_sign = "\n".join([http_method, http_uri, ACCESS_KEY, data_type, signature_version, timestamp])
    sign = base64.b64encode(hmac.new(SECRET_KEY.encode('ascii'), string_to_sign.encode('ascii'), digestmod=hashlib.sha1).digest()).decode('ascii')
    
    files = {
        'sample': sample_bytes,
    }
    data = {
        'access_key': ACCESS_KEY,
        'data_type': data_type,
        'signature_version': signature_version,
        'signature': sign,
        'sample_bytes': len(sample_bytes),
        'timestamp': timestamp
    }

    try:
        response = requests.post(f"http://{HOST}/v1/identify", files=files, data=data, timeout=10)
        response.raise_for_status()
        result = response.json()
        return result
    except:
        return None