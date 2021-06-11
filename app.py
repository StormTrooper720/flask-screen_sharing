from flask import Flask, render_template, Response
import cv2
import pyautogui
import numpy as np
from PIL import ImageGrab
screen = (0, 0)
screen += pyautogui.size()

app = Flask(__name__)


def gen_frames():
    while True:
        img = ImageGrab.grab(bbox=screen)
        img = img.resize((round(img.size[0]*.5), round(img.size[1]*.5)))
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host="10.0.0.84", port=5000)
