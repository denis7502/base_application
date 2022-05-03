from flask import Response
from flask import Flask
from flask import render_template
import threading
import datetime
import cv2
import sys
import os
sys.path.append(os.getcwd())
from client import Client
sys.path.append(os.getcwd() + '/../send_image')
from sender import Streamer
from geter import getImage
import time
import numpy as np
outputFrame = None
lock = threading.Lock()

app = Flask(__name__)

#vs = VideoStream(src=0).start()
#time.sleep(2.0)

@app.route("/")
def index():
    # return the rendered template
    return render_template("index.html")

def detect_motion():
    global outputFrame, lock
    cv_flag = True
    
    while True:
        if cv_flag:
            frame = send.frame.copy()
        else:
            frame = img.frame.copy()

        timestamp = datetime.datetime.now()
        if mqtt.msg:
            if mqtt.msg == '1':
                cv_flag = False
            elif mqtt.msg == '0':
                cv_flag = True
        if cv_flag:
            frame = send.frame.copy()
            cv2.putText(frame, 'True', (10, frame.shape[0] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)            
        else:
            frame = img.frame.copy()
            cv2.putText(frame, 'False', (10, frame.shape[0] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)            
            
        frame = cv2.putText(frame, timestamp.strftime(
            "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        with lock:
            outputFrame = frame.copy()       

def generate():
    global outputFrame, lock
    while True:
        #with lock:
        if outputFrame is None:
            continue
        (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
        if not flag:
            continue
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')            

@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
        mimetype = "multipart/x-mixed-replace; boundary=frame")  

def clean_stream():
    global outputFrame, lock
    while True:
        #with lock:
        (flag, encodedImage) = cv2.imencode(".jpg", send.frame)
        if not flag:
            continue
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n') 

@app.route("/clean_feed")
def clean_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response((clean_stream()),
        mimetype = "multipart/x-mixed-replace; boundary=frame") 

if __name__ == '__main__':
    broker = '192.168.1.192'
    port = 1883
    topic = "getAccess"
    
    mqtt = Client(broker, port, topic)
    send = Streamer('', 1)
    img = getImage(broker, port, 'videoOut')
    
    site = threading.Thread(target=detect_motion)
    
    client = threading.Thread(target=mqtt.run_subscribe)
    
    sendImg = threading.Thread(target=send.stream)
    
    video = threading.Thread(target=img.run_subscribe)
    
    #videoClear = threading.Thread(target=imgClear.run_subscribe)
    
    site.daemon = True
    
    sendImg.daemon = True

    #videoClear.daemon = True
    
    client.daemon = True
    
    video.daemon = True
    
    client.start()
    sendImg.start()
    #videoClear.start()
    video.start()
    site.start()
    
    app.run(host='192.168.1.22', port=8000, debug=True, threaded=True, use_reloader=False)

