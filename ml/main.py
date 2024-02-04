from fastapi import FastAPI, UploadFile, File
from ml.tasks.tasks import generate_random_coordinates
# from celery import Celery
# from random import choice

# celery = Celery('tasks', broker='redis://localhost:6379/0')

# @celery.task
# def generate_random_coordinates():
#     if choice([True, False]):
#         top_left_x = 100
#         top_left_y = 100
#         w = 200
#         h = 150
#         conf = 0.8
#         label = 1
#         return [top_left_x, top_left_y, w, h, conf, label]
#     else:
#         return []

app = FastAPI()

@app.post("/ml_model")
async def run_ml_model(image: UploadFile = File(...), result_code=200):
    result = generate_random_coordinates.delay()
    return {"coordinates": result}