import json
import httplib2
import socks

from flask import Flask, request


app = Flask(__name__)


@app.route('/_receive', methods=['POST'])
def hello_world():
    socks.setdefaultproxy(socks.PROXY_TYPE_HTTP, 'tasks.nginx', 80)
    socks.wrapmodule(httplib2)

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
