from ultralytics import YOLO
import cv2, time

foundObjectDir = {
    'category1': 'static/images/Library/LifeRafts',
    'category2': 'static/images/Library/LifeJackets',
    'category3': 'static/images/Library/LifeRings',
}

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

#         # img, detected_objects = add_boxes(img, toggle_switch1, toggle_switch2, toggle_switch3)

#         if detected_objects is not None:
#             for obj in detected_objects:
#                 if obj.category.name in ['person', 'life jacket', 'life ring']:
#                     messages.extend(f"{obj.category.name} at {time.strftime('%H:%M:%S')}\n")

#         ret, buffer = cv2.imencode('.jpeg', img)
#         img = buffer.tobytes()
#         yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')

