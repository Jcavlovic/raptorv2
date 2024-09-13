from fastapi import FastAPI, Request, Response, Depends
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List
from pydantic import BaseModel
from ultralytics import YOLO
#from raptor_sahi import Detect_Object, add_boxes, take_pic
import os
import cv2
import time
import threading
import subprocess

# Directory paths
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
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define input model for toggle switch route
class ToggleSwitch(BaseModel):
    switch_id: int
    state: bool

# def generate_gopro():
#     cap = cv2.VideoCapture(42)
#     cap.set(3, 1920)
#     cap.set(4, 1080)
#     start_time = time.time()

#     while True:
#         messages.clear()
#         success, img = cap.read()

#         if (time.time() - start_time) >= 1:
#             take_pic(img)
#             print('Taking photo')
#             start_time = time.time()

#         img, detected_objects = add_boxes(img, toggle_switch1, toggle_switch2, toggle_switch3)

#         if detected_objects is not None:
#             for obj in detected_objects:
#                 if obj.category.name in ['person', 'life jacket', 'life ring']:
#                     messages.extend(f"{obj.category.name} at {time.strftime('%H:%M:%S')}\n")

#         ret, buffer = cv2.imencode('.jpeg', img)
#         img = buffer.tobytes()
#         yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')

# def generate_drone():
#     drone = 'rtmp://localhost/live/test'
#     cap = cv2.VideoCapture(drone)
#     cap.set(3, 1020)
#     cap.set(4, 1080)

#     start_time = time.time()
#     while True:
#         messages.clear()
#         success, img = cap.read()

#         if (time.time() - start_time) >= 20: 
#             print('Taking Photo')
#             take_pic(img)
#             start_time = time.time()

#         img, detected_objects = add_boxes(img, toggle_switch1, toggle_switch2, toggle_switch3)

#         if detected_objects is not None:
#             for obj in detected_objects:
#                 if obj.category.name in ['person', 'life jacket', 'life ring']:
#                     messages.extend(f"{obj.category.name} at {time.strftime('%H:%M:%S')}\n")

#         ret, buffer = cv2.imencode('.jpeg', img)
#         img = buffer.tobytes()
#         yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/startpage", response_class=HTMLResponse)
async def start_page(request: Request):
    return templates.TemplateResponse("Start_page.html", {"request": request})

@app.get("/Go_Pro", response_class=HTMLResponse)
async def go_pro(request: Request):
    return templates.TemplateResponse("Go_Pro.html", {"request": request})

@app.get("/Drone_Cam", response_class=HTMLResponse)
async def drone_cam(request: Request):
    return templates.TemplateResponse("Drone_Cam.html", {"request": request})

@app.get("/Library", response_class=HTMLResponse)
async def library(request: Request):
    return templates.TemplateResponse("Library.html", {"request": request})

@app.get("/Drone_ipad", response_class=HTMLResponse)
async def drone_ipad(request: Request):
    return templates.TemplateResponse("Drone_ipad.html", {"request": request})

@app.get("/ipad", response_class=HTMLResponse)
async def start_page_ipad(request: Request):
    return templates.TemplateResponse("Start_Page_ipad.html", {"request": request})

@app.get("/gp_ipad", response_class=HTMLResponse)
async def go_pro_ipad(request: Request):
    return templates.TemplateResponse("gp_ipad.html", {"request": request})

@app.post("/switch")
async def switch(toggle: ToggleSwitch):
    global toggle_switch1, toggle_switch2, toggle_switch3
    if toggle.switch_id == 1:
        toggle_switch1 = toggle.state
    elif toggle.switch_id == 2:
        toggle_switch2 = toggle.state
    elif toggle.switch_id == 3:
        toggle_switch3 = toggle.state
    return JSONResponse(content={"success": True, "new_state": toggle.state})

# @app.get("/messages", response_model=List[str])
# async def get_messages():
#     return messages

# @app.get("/video_feed_gopro")
# async def video_feed_gopro():
    return StreamingResponse(generate_gopro(), media_type="multipart/x-mixed-replace; boundary=frame")

# @app.get("/video_feed_drone")
# async def video_feed_drone():
#     return StreamingResponse(generate_drone(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/images", response_model=List[str])
async def images():
    # Windows version (uncomment if running on Windows)
    # image_files = [f for f in os.listdir('static/images/Library/Detections') if f.endswith(('.JPG'))]
    
    # Ubuntu version
    image_files = [f for f in os.listdir('/home/raptor/Documents/raptor/static/images/Library/Detections') if f.endswith(('.JPG', '.jpg'))]
    return image_files

@app.get("/images/{filename}")
async def image(filename: str):
    file_path = f"/home/raptor/Documents/raptor/static/images/Library/Detections/{filename}"
    return FileResponse(path=file_path)

@app.get("/library_images", response_model=List[str])
async def images_library(category: List[str]):
    image_paths = []
    for cat in category:
        image_dir = IMAGE_DIRS.get(cat)
        if image_dir:
            image_files = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]
            image_paths.extend([os.path.join(image_dir, file) for file in image_files])
    return image_paths

def start_gopro():
    command = ['sudo', 'gopro', 'webcam', '-a', '-n']
    subprocess.run(command)
