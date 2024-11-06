# Working YOLOv8 with SAHI 
# Check save dir for new photo to test, run inference, then sort image of each detected object into directory for the object type.
# Crafted by Cavlovic with love.

import time
import os
import datetime
import cv2
import math
import numpy as np
import subprocess

from PIL import Image,  ImageDraw, ImageFont
from ultralytics import YOLO
from sahi.utils.cv import visualize_object_predictions,read_image_as_pil
from sahi.utils.yolov8 import download_yolov8s_model
from sahi import AutoDetectionModel
from sahi.utils.cv import read_image
from sahi.utils.file import download_from_url
from sahi.predict import get_prediction, get_sliced_prediction, predict
from pathlib import Path

global detected_objects
detected_objects =  []

destination_dir = '/home/raptor/Documents/raptor/static/images/Library/Detections'
destination_dir2 = '/home/raptor/Documents/raptor/static/images/Library'
destination_dir3 = '/home/raptor/Pictures/Saved Images'

#raptor_model_path = 'static/model/raptor_v5m.pt'
yolov8_model_path = 'static/model/yolov8m.pt'

# Import model to use for detection.
detection_model = AutoDetectionModel.from_pretrained(
model_type='yolov8',
model_path=yolov8_model_path,
confidence_threshold=0.5,
device="cuda:0", # or 'cpu'
)

save_img = '/home/raptor/Documents/raptor/static/images/inference/test.jpg'

font = cv2.FONT_HERSHEY_PLAIN
fontScale = 1.5
color = (255, 255, 0)
thickness = 2

def save_array(objects):
    global detected_objects
    detected_objects = objects

def return_array():

    return detected_objects

def Detect_Object():

    object_count_Buffer = [-1, -1, -1]
    i = 0 

    while True:
        
        object_Count = [0, 0, 0]
        
        while not os.path.isfile(save_img):
            foo = None

        time.sleep(1)
        img = cv2.imread(save_img, cv2.IMREAD_UNCHANGED)
        print('Running Inference')
        # Settings for SAHI. 640x480 with zero overlay, best settings for speed.
        start = time.time()
        result = get_sliced_prediction(
            img,
            detection_model,
            slice_height = 640,
            slice_width = 640,
            overlap_height_ratio = 0,
            overlap_width_ratio = 0.7,
            perform_standard_pred = False,
            verbose = 0
        )
        time1 = time.time() - start


        save_array(result.object_prediction_list)

        # Crop image with found objects cords and sort into folders for each category.
        # Checks if the same number of objects are detected to eliminate duplicate images.
        # Saves images with the name formated "ObjectDetected_TimeOfDetection", ie LifeRaft_12:30:00


#        for objects in result.object_prediction_list :
#
#            current_time = datetime.datetime.now().time().strftime('%H.%M.%S')
#
#            if objects.category.name == 'person':
#                object_Count[0] += 1
#            elif objects.category.id == 1:
#                object_Count[1] += 1
#            elif objects.category.id == 2:
#                object_Count[2] += 1
#            
#                
#            if objects.category.name == "person" and object_Count[0] is not object_count_Buffer[0]:
#
#                object_cords = result.object_prediction_list[0].bbox.to_xywh()
#                x = int(object_cords[0]) + int(object_cords[2])
#                y = int(object_cords[1]) + int(object_cords[3])
#                cropped_image = img[int(object_cords[1]):y,int(object_cords[0]):x]
#                confidence = int(objects.score.value*100)
#                text = f'Person({i}).{confidence}.{current_time}'
#                destination = f'{destination_dir}/Person({i}) {current_time}.jpg'
#                destination2 = f'{destination_dir2}/LifeJackets/Person({i}) {current_time}.jpg'
#
#                cv2.putText(cropped_image, text, (10, 20), font, fontScale, color, thickness)
#
#                cv2.imwrite(destination, cropped_image)
#                cv2.imwrite(destination2, cropped_image)
#
            # Life_Ring
#            elif objects.category.name == "life jacket" and object_Count[1] is not object_count_Buffer[1]:
#                
#                object_cords = result.object_prediction_list[0].bbox.to_xywh()
#                x = int(object_cords[0]) + int(object_cords[2])
#                y = int(object_cords[1]) + int(object_cords[3])
#                cropped_image = img[int(object_cords[1]):y,int(object_cords[0]):x]
#                confidence = int(objects.score.value*100)
#                text = 'LifeJacket({i}).{confidence}.{current_time}'
#                destination = "{destination_dir}/{text}.jpg"
#                destination2 = "{destination_dir2}/LifeJacket/LifeJacket({i}) {current_time}.jpg"
#
#                cv2.putText(cropped_image, text , (10, 10), font, fontScale, color, thickness)
#
#                cv2.imwrite(destination, cropped_image)
#                cv2.imwrite(destination2, cropped_image)
#
            # Life_Raft
#            elif objects.category.name == "life raft" and object_Count[2] is not object_count_Buffer[2]:
#                
#                object_cords = result.object_prediction_list[0].bbox.to_xywh()
#                x = int(object_cords[0]) + int(object_cords[2])
#                y = int(object_cords[1]) + int(object_cords[3])
#                cropped_image = img[int(object_cords[1]):y,int(object_cords[0]):x]
#                confidence = int(objects.score.value*100)
   #             text = 'LifeRaft{i}).{confidence}.{current_time}'
  #              destination = "{destination_dir}/{text}.jpg"
 #               destination2 = "{destination_dir2}/LifeRafts/LifeRaft({i}) {current_time}.jpg"
#
 #               cv2.putText(cropped_image, text , (10, 10), font, fontScale, color, thickness)
#
 #               cv2.imwrite(destination, cropped_image)
#                cv2.imwrite(destination2, cropped_image)

        object_count_Buffer = object_Count
        try:
            os.remove(save_img)
        except:
            foo = None

def take_pic(img):

    try:
        cv2.imwrite(save_img, img)
    except:
        foo=None
def add_boxes(img, toggle_switch1, toggle_switch2, toggle_switch3):

    objects = return_array()

    for object in objects: 
        object_name = object.category.name
        current_time = datetime.datetime.now().time().strftime('%H.%M.%S')

        if toggle_switch1 is True:
            if object_name == 'person':
                x1, y1, x2, y2 = object.bbox.to_xyxy()
                x1, y1, x2, y2 = int((int(x1))), int((int(y1))), int((int(x2))), int((int(y2))) # convert to int values
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 0), 3)
                org = [x1, (y1 - 10)]
                cv2.putText(img, "person" + " " + str(int(object.score.value*100)) + "% " + str(current_time) , org, font, fontScale, color, thickness)
            
        if toggle_switch2 is True:
            if object_name == 'life jacket':
                x1, y1, x2, y2 = object.bbox.to_xyxy()
                x1, y1, x2, y2 = int((int(x1))), int((int(y1))), int((int(x2))), int((int(y2))) # convert to int values
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 0), 3)
                org = [x1, (y1 - 10)]
                cv2.putText(img, "Life Jacket" + " " + str(int(object.score.value*100)) + "% " + str(current_time) , org, font, fontScale, color, thickness)

        if toggle_switch3 is True:
            if object_name == 'life ring':
                x1, y1, x2, y2 = object.bbox.to_xyxy()
                x1, y1, x2, y2 = int((int(x1))), int((int(y1))), int((int(x2))), int((int(y2))) # convert to int values
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 0), 3)
                org = [x1, (y1 - 10)]
                cv2.putText(img, "Life Ring" + " " + str(int(object.score.value*100)) + "% " + str(current_time) , org, font, fontScale, color, thickness)

    return img, objects