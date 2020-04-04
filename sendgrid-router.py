import json
import subprocess
from flask import Flask, request, Response


app = Flask(__name__)

# proxy = 'http://localhost:80'
proxy = None


@app.route('/_receive', methods=['POST'])
def event_receive():
    events = json.loads(request.data.decode('utf-8'))
    for event in events:
        if 'source-callback' in event:
            callback_url = event['source-callback']
            if proxy:
                subprocess.check_output([
                    'curl', '-X', 'POST', '--proxy', proxy, '-d', json.dumps(event), callback_url
                ])
            else:
                subprocess.check_output([
                    'curl', '-X', 'POST', '-d', json.dumps(event), callback_url
                ])

    return Response(status_code=200)


if __name__ == '__main__':
    app.run()
