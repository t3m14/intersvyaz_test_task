
from celery import Celery
import requests
from app.database.auto_ml import create_auto
from app.config import ML_URL
celery = Celery('tasks', broker='redis://redis:6379/0')


@celery.task
def resize_and_convert_to_base64(image):
    import cv2
    import base64
    import numpy as np
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
    resp = requests.post(ML_URL)
    data = resp.json()
    return data["coordinates"]
@celery.task
def save_to_db(detected_box):
    from app.database.database import get_db
    db = get_db()

    # Сохранение информации в БД
    if detected_box:
        create_auto(is_detected=True, x_coord=detected_box[0], y_coord=detected_box[1],w=detected_box[2], h=detected_box[3], db=db)
    else:
        create_auto(is_detected=False, db=db)
