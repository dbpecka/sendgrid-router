import json
import httplib2

from flask import Flask, request


app = Flask(__name__)


@app.route('/_receive', methods=['POST'])
def hello_world():
    http = httplib2.Http()

    events = json.loads(request.data.decode('utf-8'))
    for event in events:
        print(json.dumps(event))
        if 'source-callback' in event:
            callback = event['source-callback']
            http.request(callback, 'POST', json.dumps(event))

    return 'Ack'


if __name__ == '__main__':
    app.run()
