import json
import subprocess

from flask import Flask, request


app = Flask(__name__)


@app.route('/_receive', methods=['POST'])
def hello_world():
    events = json.loads(request.data.decode('utf-8'))
    for event in events:
        print(json.dumps(event))

        if 'source-callback' in event:
            callback_url = event['source-callback']
            subprocess.check_output([
                'curl', '-X', 'POST', '--proxy', 'http://tasks.nginx:80', '-d', json.dumps(event), callback_url
            ])

    return 'Ack'


if __name__ == '__main__':
    app.run()
