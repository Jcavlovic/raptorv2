
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask import Response
from ultralytics import YOLO
from raptor_sahi import Detect_Object, add_boxes, take_pic
from collections import deque

import shutil
import os
import cv2
import math
import time
import threading
import datetime
import subprocess

# LINUX DIRECTORY
IMAGE_DIRS = {
    'category1': 'static/images/Library/LifeRafts',
    'category2': 'static/images/Library/LifeJackets',
    'category3': 'static/images/Library/LifeRings',
}

toggle_switch1 = True
toggle_switch2 = True
toggle_switch3 = True

messages = []
objects_buffer = []

app = Flask(__name__)

def generate_gopro():

    cap = cv2.VideoCapture(42)
    cap.set(3, 1920)
    cap.set(4, 1080)
    start_time = time.time()

    while True:
        messages.clear()
        success, img = cap.read()

        if (time.time() - start_time) >= 1:
            take_pic(img)
            print('Taking photo')
            start_time = time.time()
        
        img, detected_objects = add_boxes(img, toggle_switch1, toggle_switch2, toggle_switch3)

        if detected_objects is not None:
            for objects in detected_objects:
                if objects.category.name == 'person':
                    messages.extend(f"{objects.category.name} at {time.strftime('%H:%M:%S')}\n")
                elif objects.category.name == 'life jacket':
                    messages.extend(f"{objects.category.name} at {time.strftime('%H:%M:%S')}\n")
                elif objects.category.name == 'life ring':
                    messages.extend(f"{objects.category.name} at {time.strftime('%H:%M:%S')}\n")

        try:
            ret, buffer = cv2.imencode('.jpeg', img)
            img = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')  
        except:
            foo = None
        
def generate_drone():

    drone = 'rtmp://localhost/live/test'
    cap = cv2.VideoCapture(drone)
    cap.set(3, 1020)
    cap.set(4, 1080)

    start_time = time.time()
    while True:
        messages.clear()
        success, img = cap.read()

        if (time.time() - start_time) >=20: 
            print('Taking Photo')
            take_pic(img)

            start_time = time.time()
        
        img, detected_objects = add_boxes(img, toggle_switch1, toggle_switch2, toggle_switch3)

        if detected_objects is not None:
            for objects in detected_objects:
                if objects.category.name == 'person':
                    messages.extend(f"{objects.category.name} at {time.strftime('%H:%M:%S')}\n")
                elif objects.category.name == 'life jacket':
                    messages.extend(f"{objects.category.name} at {time.strftime('%H:%M:%S')}\n")
                elif objects.category.name == 'life ring':
                    messages.extend(f"{objects.category.name} at {time.strftime('%H:%M:%S')}\n")

        try:
            ret, buffer = cv2.imencode('.jpeg', img)
            img = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')  
        except:
            foo = None

#Andrew Garza          
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/startpage')
def startPage():
    return render_template('Start_page.html')

#Andrew Garza  
@app.route('/Go_Pro')
def goPro():
    return render_template('Go_Pro.html')

#Andrew Garza    
@app.route('/Drone_Cam')
def droneCam():
    return render_template('Drone_Cam.html')

#Andrew Garza
@app.route('/Library')
def Library():
    return render_template('Library.html')

#Andrew Garza  
@app.route('/Drone_ipad')
def goPro_iPad():
    return render_template('Drone_ipad.html')

#Andrew Garza  
@app.route('/ipad')
def startPage_iPad():
    return render_template('Start_Page_ipad.html')

#Andrew Garza    
@app.route('/gp_ipad')
def go_Pro_iPad():
    return render_template('gp_ipad.html')

#Andrew Garza 
show_images_from_folder = False

#Jordan Cavlovic
@app.route('/switch', methods=['POST',])
def switch():
    global toggle_switch1, toggle_switch2, toggle_switch3
    switch_id = request.json['switch_id']
    state = request.json['state']
    if switch_id == 1:
        toggle_switch1 = state
    elif switch_id == 2:
        toggle_switch2 = state
    elif switch_id == 3:
        toggle_switch3 = state
    return jsonify({"success": True, "new_state": state})

@app.route('/messages', methods=['GET'])
def get_messages():
    global messages
    return jsonify(list(messages))

# Andrew Garza 03/11/24
@app.route('/video_feed_gopro')
def video_gopro():
    return Response(generate_gopro(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_drone')
def video_drone():
    return Response(generate_drone(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/images')
def images():

    # WINDOWS   
    # image_files = [f for f in os.listdir('static/images/Library/Detections') if f.endswith(('.JPG'))]
    # UBUNTU
    image_files = [f for f in os.listdir('/home/raptor/Documents/raptor/static/images/Library/Detections') if f.endswith(('.JPG', '.jpg'))]

    return jsonify(image_files) 

@app.route('/images/<filename>')
def image(filename):

    # WINDOWS
    # return send_from_directory('static/images/Library/Detections', filename)
    # UBTUNTU
    return send_from_directory('/home/raptor/Documents/raptor/static/images/Library/Detections', filename) 

@app.route('/library_images')
def images_library():
    categories = request.args.getlist('category')
    image_paths = []
    for category in categories:
        image_dir = IMAGE_DIRS.get(category)
        if image_dir:
            image_files = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]
            image_paths.extend([os.path.join(image_dir, file) for file in image_files])
    return jsonify(image_paths)     


def start_gopro():
    command = ['sudo', 'gopro', 'webcam', '-a', '-n']
    subprocess.run(command)     

if __name__ == '__main__':
    thread = threading.Thread(target=Detect_Object)
#    thread2 = threading.Thread(target=start_gopro)
#    thread2.start()
#    time.sleep(20)
    thread.start()

    app.run('0.0.0.0', port=5000, debug=False)