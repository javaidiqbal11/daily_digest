# main
import os, requests

api = 'https://api.aldea.ai/v1/listen'
token = 'org_HyTc5-RgfIZ9o6FizjHe_rjZeb46aMokDdzGQeZtnVZxIeAjg6iMN1Azs19XY_bidU-kcfpC8t1nnZiAMHuFJPQyqhAXymu9txnfV0jf3DY02KP3xB7oRlTIrlYaJL9q' # optional if auth disabled

with open('aldea_sample.wav', 'rb') as f:
    headers = {
        **({'Authorization': f'Bearer {token}'} if token else {}),
    }
    r = requests.post(api, headers=headers, data=f)
    r.raise_for_status()
    print(r.json())

