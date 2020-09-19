from flask import Flask, render_template, Response, request
import cv2
import processing

app = Flask(__name__)
video = cv2.VideoCapture(0)


@app.route('/')
def index():
    # renders the web page
    return render_template('index.html')


@app.route('/take_image', methods=['POST'])
def take_image():
    name = request.form['name']
    # print(name)
    _, frame = video.read()

    cv2.imwrite(f'{name}.jpg', frame)
    processing.process_image(f'{name}.jpg')

    return Response(status=200)


def gen():
    """Video streaming generator function."""
    while True:
        rval, frame = video.read()
        cv2.imwrite('t.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    # defining the server ip address and port
    app.run(host='0.0.0.0', port='5000', debug=True)
