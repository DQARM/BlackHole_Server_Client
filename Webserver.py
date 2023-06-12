from flask import Flask, Response, request
import os

app = Flask(__name__)

@app.route('/data')
def data_file():
    size = request.args.get('size', default = 1, type = int) # size in MB
    size *= 1024 * 1024 # convert to bytes

    def generate():
        data_size = 1024 # 1 KB
        for _ in range(size // data_size):
            yield os.urandom(data_size)

    response = Response(generate(), mimetype='application/octet-stream')
    response.headers.set('Content-Disposition', 'attachment', filename='data')
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8000)
