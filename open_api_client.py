import hashlib
import json
from typing import Dict
import requests


class Client:
    def __init__(self, endpoint: str, app_id: str, secret: str):
        self.endpoint = endpoint
        self.app_id = app_id
        self.secret = secret

    def get_sign(self, body: Dict):
        kvs = []
        for key, value in body.items():
            if value is not None and key != "sign":
                kvs.append(key + '=' + (value if type(value) ==
                           str else json.dumps(value, ensure_ascii=False, separators=(',', ':'))))
        to_encode_str = "&".join(sorted(kvs))
        to_encode_str = to_encode_str + '&key=' + self.secret
        m = hashlib.md5()
        m.update(to_encode_str.encode("utf-8"))
        return m.hexdigest().upper()

    def request(self, path: str, data: Dict, nonce_str: str = '1593359464730'):
        data['appid'] = self.app_id
        data['nonce_str'] = nonce_str
        data['sign'] = self.get_sign(data)

        url = f'{self.endpoint}/{path.lstrip("/")}'
        # if path == '/repo/commit/list':
        #     print(f"data = {data}")
        #     print(f"url = {url}")

        response = requests.post(url, json=data)
        if response.status_code != 200:
            raise Exception(f"request got a error: {response}")
        result = response.json()
        return result['code'], result['message'], result.get('data', None)
