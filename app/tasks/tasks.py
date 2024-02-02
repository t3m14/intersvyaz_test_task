import cv2
import base64
import numpy as np
from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379/0')



@celery.task
def resize_and_convert_to_base64(image):
    # Преобразовать изображение в numpy-массив
    np_array = np.frombuffer(image, np.uint8)
    img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    # Изменить размер изображения до 640x640
    img_resized = cv2.resize(img, (640, 640))

    # Нормализовать изображение
    img_normalized = cv2.normalize(img_resized, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    # Преобразовать обработанное изображение в base64-строку
    _, img_base64 = cv2.imencode('.jpg', img_normalized)
    base64_str = base64.b64encode(img_base64.tobytes())

    return base64_str

@celery.task
def run_ml_model(processed_image):
    # Имитация работы модели машинного обучения
    # TODO: реализовать логику работы модели
    return [100, 100, 200, 200, 0.9, 1]  # Пример координат бокса автомобиля

@celery.task
def save_to_db(detected_box):
    # Сохранение информации в БД
    # TODO: реализовать сохранение в БД
    pass
