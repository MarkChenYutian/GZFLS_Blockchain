import json
import requests

content = {'content': 'h1111'}
r = requests.post("http://127.0.0.1:5000", json=content)
print(json.dumps(content))
print(r.text)
