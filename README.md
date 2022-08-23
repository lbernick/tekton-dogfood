Steps:
- [Create Github App](https://docs.github.com/en/developers/apps/building-github-apps/creating-a-github-app)
  - Must have read and write permissions to "Checks" API
  - Must subscribe to "Check suite" and "Check run" events
  - Use eventlistener exernal IP for webhook address
  - Create a private key for the app
- Install Github App on repo
- Get app ID and installation ID
- Generate a JSON web token

- Create a new Check
  - Open a PR on the repo
  - Get the SHA of the commit for this PR
  - Make a create check request:
```
curl -i -H "Authorization: Bearer ${JWT}" -H "Accept: application/vnd.github+json" https://api.github.com/repos/{org-or-user}/{repo-name}/check-runs -d '{"name":"ci","head_sha":"${SHA}","status":"in_progress"}'
```

## Generating a JSON web token

### Running directly
```sh
python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
python3 jwt/jwt.py -p <path-to-private-key-file> -a <application-id> -i <installation-id> -c <cache-file>
```

### Using docker
```sh
docker build jwt -t jwt
docker run -v <path-to-private-key-file>:/github-private-key jwt -p /github-private-key
```