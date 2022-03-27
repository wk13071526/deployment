from flask import Flask, request, jsonify
import json
import time
import logging
import base64
import numpy as np
import traceback
import six
from src import deployment

app = Flask(__name__)
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='deployment.log', level=logging.DEBUG, format=LOG_FORMAT)


@app.route('/health')
def heart_beat():
    return jsonify({'status': 'UP'})


@app.route('/pipe', methods=['POST'])
def pipe():
    return get_response()


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


def get_response():
    try:
        start_time = time.time()
        result = call_algorithm()
        duration = time.time() * 1000 - start_time * 1000
        logging.info('apply cost: %s ms', duration)
        if is_binary(result):
            content_type = 'binary'
            result = base64.b64encode(result)
            # In python 3, the encoded result is a byte array which cannot be
            # json serialized, so we need to turn this into a string.
            if not isinstance(result, six.string_types):
                result = str(result, 'utf-8')
        elif isinstance(result, six.string_types) or isinstance(result, six.text_type):
            content_type = 'text'
        else:
            content_type = 'json'
        response_string = json.dumps({
            'result': result,
            'metadata': {
                'duration': duration,
                'content_type': content_type
            }
        }, ensure_ascii=False, cls=NumpyEncoder)
    except Exception as e:
        if hasattr(e, 'error_type'):
            error_type = e.error_type
        else:
            error_type = 'ModelError'
        response_string = json.dumps({
            'error': {
                'message': str(e),
                'stacktrace': traceback.format_exc(),
                'error_type': error_type
            }
        }, ensure_ascii=False)
        logging.error("[Exception] %s", response_string)
    return response_string


def call_algorithm():
    content_type = request.content_type
    logging.info("request contentType: %s ,content_length: %d", content_type, request.content_length)
    if content_type.startswith("application/json"):
        data = request.get_json()
    elif content_type.startswith('text/plain'):
        if is_binary(request.get_data()):
            data = request.get_data().decode('utf-8')
        else:
            data = request.get_data()
    elif content_type == 'application/octet-stream' or content_type == 'binary':
        data = wrap_binary_data(request.data)
    else:
        raise Exception("Invalid content_type: {}".format(content_type))
    result = deployment.apply(data)
    return result


def is_binary(arg):
    return isinstance(arg, base64.bytes_types)


def wrap_binary_data(data):
    return bytes(data)


# np array转json
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


if __name__ == '__main__':
    app.run()
