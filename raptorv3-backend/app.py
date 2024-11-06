from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from ultralytics import YOLO
from raptor import Detect_Object, add_boxes, take_pic
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

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

class SwitchState(BaseModel):
    switch_id: int
    state: bool

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

        if (time.time() - start_time) >= 20: 
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

@app.get("/")
async def index():
    return {"message": "Hello, FastAPI!"}

@app.get("/startpage")
async def start_page():
    return {"message": "Start Page"}

@app.get("/Go_Pro")
async def go_pro():
    return {"message": "Go Pro"}

@app.get("/Drone_Cam")
async def drone_cam():
    return {"message": "Drone Camera"}

@app.get("/Library")
async def library():
    return {"message": "Library"}

@app.get("/Drone_ipad")
async def go_pro_ipad():
    return {"message": "Drone iPad"}

@app.get("/ipad")
async def start_page_ipad():
    return {"message": "Start Page iPad"}

@app.get("/gp_ipad")
async def go_pro_ipad():
    return {"message": "Go Pro iPad"}

@app.post("/switch")
async def switch(switch_state: SwitchState):
    global toggle_switch1, toggle_switch2, toggle_switch3
    if switch_state.switch_id == 1:
        toggle_switch1 = switch_state.state
    elif switch_state.switch_id == 2:
        toggle_switch2 = switch_state.state
    elif switch_state.switch_id == 3:
        toggle_switch3 = switch_state.state
    return {"success": True, "new_state": switch_state.state}

@app.get("/messages")
async def get_messages():
    return JSONResponse(content=messages)

@app.get("/video_feed_gopro")
async def video_gopro():
    return StreamingResponse(generate_gopro(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/video_feed_drone")
async def video_drone():
    return StreamingResponse(generate_drone(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/images")
async def images():
    image_files = [f for f in os.listdir('/home/raptor/Documents/raptor/static/images/Library/Detections') if f.endswith(('.JPG', '.jpg'))]
    return JSONResponse(content=image_files)

@app.get("/images/{filename}")
async def image(filename: str):
    return Response(content=open(f"/home/raptor/Documents/raptor/static/images/Library/Detections/{filename}", "rb").read(), media_type="image/jpeg")

@app.get("/library_images")
async def images_library(request: Request):
    categories = request.query_params.getlist('category')
    image_paths = []
    for category in categories:
        image_dir = IMAGE_DIRS.get(category)
        if image_dir:
            image_files = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]
            image_paths.extend([os.path.join(image_dir, file) for file in image_files])
    return JSONResponse(content=image_paths)

def start_gopro():
    command = ['sudo', 'gopro', 'webcam', '-a', '-n']
    subprocess.run(command)

if __name__ == '__main__':
    thread = threading.Thread(target=Detect_Object)
    thread.start()
