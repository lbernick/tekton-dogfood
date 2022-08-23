#!/usr/bin/env python3
import argparse
import base64
import datetime
import json
import os
import subprocess
import time

import requests
from jwcrypto import jwk, jwt

EXPIRE_MINUTES_AS_SECONDS = int(
    os.environ.get('GITHUBAPP_TOKEN_EXPIRATION_MINUTES', 10)) * 60
GITHUB_API_URL = "https://api.github.com"


class GitHub():
    token = None

    def __init__(self,
                 private_key,
                 app_id,
                 expiration_time,
                 github_api_url,
                 installation_id=None):
        if not isinstance(private_key, bytes):
            raise ValueError(f'"{private_key}" parameter must be byte-string')
        self._private_key = private_key
        self.app_id = app_id
        self.expiration_time = expiration_time
        self.token = self._app_token()
        self.github_api_url = github_api_url
        self.token = self._get_token(installation_id)

    def _load_private_key(self, pem_key_bytes):
        return jwk.JWK.from_pem(pem_key_bytes)

    def _app_token(self):
        key = self._load_private_key(self._private_key)
        now = int(time.time())

        token = jwt.JWT(
            header={"alg": "RS256"},
            claims={
                "iat": now,
                "exp": now + self.expiration_time,
                "iss": int(self.app_id),
            },
            algs=["RS256"],
        )
        token.make_signed_token(key)
        return token.serialize()

    def _get_token(self, installation_id=None):
        app_token = self._app_token()
        if not installation_id:
            return app_token
        req = self._request(
            "POST",
            f"/app/installations/{installation_id}/access_tokens",
            headers={
                "Authorization": f"Bearer {app_token}",
                "Accept": "application/vnd.github.v3+json"
            })

        if not req.text.strip():
            raise Exception("Not getting a json: code: %s reason: %s" %
                            (req.status_code, req.reason))
        ret = req.json()
        if 'token' not in ret:
            raise Exception("Authentication errors: %s" % (req.text))

        return ret['token']

    def _request(self, method, url, headers={}, data={}):
        if self.token and 'Authorization' not in headers:
            headers.update({"Authorization": "Bearer " + self.token})
        if not url.startswith("http"):
            url = f"{self.github_api_url}{url}"
        return requests.request(method,
                                url,
                                headers=headers,
                                data=json.dumps(data))

def get_private_key(path):
    with open(path, 'rb') as f:
        return f.read()

def main(args):
    if args.cache_file and os.path.exists(args.cache_file):
        mtime = os.path.getmtime(args.cache_file)
        if datetime.datetime.fromtimestamp(mtime) < datetime.datetime.now(
        ) - datetime.timedelta(seconds=args.token_expiration_time):
            os.remove(args.cache_file)
        else:
            print(open(args.cache_file).read())
            return

    private_key = get_private_key(args.private_key_path)
    github_app = GitHub(private_key,
                        app_id=args.app_id,
                        expiration_time=args.token_expiration_time,
                        github_api_url=GITHUB_API_URL,
                        installation_id=args.installation_id)
    if args.cache_file:
        open(args.cache_file, "w").write(github_app.token)
    else:
        print(github_app.token)


def parse_args():
    parser = argparse.ArgumentParser(description='Generate a user token')
    parser.add_argument("--token-expiration-time",
                        type=int,
                        help="Token expiration time (seconds)",
                        default=EXPIRE_MINUTES_AS_SECONDS)
    parser.add_argument("-p",
                        "--private-key-path",
                        help="Path to private key",
                        required=True)
    parser.add_argument("-a", "--app-id", help="Github Application ID", default="229835")
    parser.add_argument("--installation-id",
                        "-i",
                        type=int,
                        help="Installation_ID",
                        default="28405964")
    parser.add_argument(
        "-c",
        "--cache-file",
        help=("Cache file will only regenerate after the expiration time,"
              " default: %d minutes") % (EXPIRE_MINUTES_AS_SECONDS / 60),
        default=os.environ.get("GITHUBAPP_RESULT_PATH"))
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_args())