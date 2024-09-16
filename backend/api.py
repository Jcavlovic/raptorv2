from fastapi import FastAPI, Request, Response, Depends
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse, FileResponse
from pydantic import BaseModel
from raptorv2.backend.detection.detection import foundObjectDir
from fastapi.middleware.cors import CORSMiddleware

class SwitchState(BaseModel):
    switch1 : bool
    switch2 : bool
    switch3 : bool

switch_states = {
    "switch1": False, 
    "switch2": False, 
    "switch3":False
    }

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "http://192.168.1.23:3000",
    "192.168.1.23:3000"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to the raptor backend, please don't break me."}

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