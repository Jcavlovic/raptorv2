from fastapi import FastAPI, Request, Response, Depends
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List
from pydantic import BaseModel
import os
from detection import foundObjectDir
from fastapi.middleware.cors import CORSMiddleware

class SwitchState(BaseModel):
    switch1 : bool
    switch2 : bool
    switch3 : bool

switch_states = {"switch1": False, "switch2": False, "switch3":False} 

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "http://192.168.1.23:3000",
    "192.168.1.23:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Define input model for toggle switch route
class ToggleSwitch(BaseModel):
    switch_id: int
    state: bool


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your todo list."}

@app.get("/switches")
async def get_switches():
    return switch_states

@app.post("/switches")
async def set_switches(state: SwitchState):
    switch_states["switch1"] = state.switch1
    switch_states["switch2"] = state.switch2
    switch_states["switch3"] = state.switch3
    print(switch_states)
    return switch_states

# @app.get("/images", response_model=List[str])
# async def images():
    

#     image_files = [f for f in os.listdir('/home/raptor/Documents/raptor/static/images/Library/Detections') if f.endswith(('.JPG', '.jpg'))]
#     return image_files

# @app.get("/images/{filename}")
# async def image(filename: str):
#     file_path = f"/home/raptor/Documents/raptor/static/images/Library/Detections/{filename}"
#     return FileResponse(path=file_path)

# @app.get("/library_images", response_model=List[str])
# async def images_library(category: List[str]):
#     image_paths = []
#     for cat in category:
#         image_dir = foundObjectDir.get(cat)
#         if image_dir:
#             image_files = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]
#             image_paths.extend([os.path.join(image_dir, file) for file in image_files])
#     return image_paths
