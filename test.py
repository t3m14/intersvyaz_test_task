from fastapi.testclient import TestClient
from app.main import app as app_app
from ml.main import app as app_ml
from ml.main import generate_random_coordinates
from unittest.mock import patch, Mock

client_ml = TestClient(app_ml)
client_app = TestClient(app_app)



def test_process_image():
    # Подготовка данных для отправки запроса
    image_bytes = b'fake_image_bytes'
    response = client_app.post("/piplines", json={"name": "Test Pipeline"})
    data = response.json()
    pipeline_id = data["id"]
    step1 = client_app.post(f"/piplines/{pipeline_id}/steps", json={"name": "resize_and_convert_to_base64", "order": "1"})
    step2 = client_app.post(f"/piplines/{pipeline_id}/steps", json={"name": "run_ml_model", "order": "2"})
    step3 = client_app.post(f"/piplines/{pipeline_id}/steps", json={"name": "save_to_db", "order": "3"})

    with patch("app.tasks.tasks.resize_and_convert_to_base64") as mock_resize, patch("app.tasks.tasks.run_ml_model") as mock_ml, patch("app.tasks.tasks.save_to_db") as mock_save:
        # Устанавливаем возвращаемые значения при вызове Celery tasks
        mock_resize.return_value = Mock(id="resize_task_id")
        mock_ml.return_value = Mock(id="ml_task_id")
        mock_save.return_value = Mock(id="save_task_id")

        # Отправка запроса на обработку изображения
        response = client_app.post(f"/process_image/{pipeline_id}", files={"image": ("test.jpg", image_bytes)})

    # Проверка успешности ответа
    assert response.json() == {"message": "Image processed successfully"}
    assert response.status_code == 200

    # Проверка вызовов задач
    mock_resize.assert_called_once_with(image_bytes, pipeline_id)
    mock_ml.assert_called_once_with("resize_task_id")
    mock_save.assert_called_once_with("ml_task_id")
    
def test_create_pipeline():
    response = client_app.post("/piplines", json={"name": "Test Pipeline"})
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "id" in data

def test_get_pipelines():
    response = client_app.get("/piplines")
    assert response.status_code == 200
    data = response.json()
    assert data != []

def test_get_pipeline_by_id():
    response = client_app.post("/piplines", json={"name": "Test Pipeline"})
    data = response.json()
    pipeline_id = data["id"]
    
    response = client_app.get(f"/piplines/{pipeline_id}")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data

def test_delete_pipeline():
    response = client_app.post("/piplines", json={"name": "Test Pipeline"})
    data = response.json()
    assert "id" in data

    pipeline_id = data["id"]
    
    response = client_app.delete(f"/piplines/{pipeline_id}")  # передача объекта Pipline в качестве зависимости
    assert response.status_code == 200


# Тесты для steps 
def test_create_step():
    response = client_app.post("/piplines", json={"name": "Test Pipeline"})
    data = response.json()
    pipeline_id = data["id"]
    response = client_app.post(f"/piplines/{pipeline_id}/steps", json={"name": "Test Step", "order": 1})
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "order" in data

def test_get_steps_by_pipeline():
    response = client_app.post("/piplines", json={"name": "Test Pipeline"})
    data = response.json()
    pipeline_id = data["id"]
    response = client_app.post(f"/piplines/{pipeline_id}/steps", json={"name": "Test Step", "order": 1})
    response = client_app.get(f"/piplines/{pipeline_id}/steps")
    assert response.status_code == 200
    data = response.json()
    assert data != []

def test_get_step_by_id():
    pipline = client_app.post("/piplines", json={"name": "Test Pipeline"})
    pipeline_data = pipline.json()
    pipeline_id = pipeline_data["id"]
    step = client_app.post(f"/piplines/{pipeline_id}/steps", json={"name": "Test Step", "order": "1"})
    step_data = step.json()
    step_id = step_data["id"]

    response = client_app.get(f"/piplines/{pipeline_id}/steps/{step_id}")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "order" in data

def test_edit_step():
    response = client_app.post("/piplines", json={"name": "Test Pipeline"})
    data = response.json()
    pipeline_id = data["id"]
    response = client_app.post(f"/piplines/{pipeline_id}/steps", json={"name": "Test Step", "order": 2})
    data = response.json()
    step_id = data["id"]

    response = client_app.put(f"/piplines/{pipeline_id}/steps/{step_id}", json={"name": "Updated Step", "order": 1})
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "order" in data

def test_delete_step():
    response = client_app.post("/piplines", json={"name": "Test Pipeline"})
    data = response.json()
    pipeline_id = data["id"]
    response = client_app.post(f"/piplines/{pipeline_id}/steps", json={"name": "Test Step", "order": 1})
    data = response.json()
    step_id = data["id"]

    response = client_app.delete(f"/piplines/{pipeline_id}/steps/{step_id}")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "order" in data



def test_run_ml_model_with_image():
        file_path = "./test.jpg"
        file = open(file_path, "rb")
        response = client_ml.post(
        "/ml_model", files={"image": ("filename", file, "image/jpeg")}
        )   
        assert "coordinates" in response.json()
        assert response.status_code == 200

def test_run_ml_model_without_image():
    response = client_ml.post("/ml_model")
    assert response.status_code == 422

def test_generate_random_coordinates():
    result = generate_random_coordinates()
    assert result is not None
    assert len(result) == 0 or len(result) == 6
    if len(result) == 6:
        assert all(isinstance(coord, (int, float)) for coord in result[:-1])
        assert 0 <= result[4] <= 1  # Checking confidence value
        assert result[5] == 1  # Making sure the label is 1
    with patch("app.tasks.tasks.resize_and_convert_to_base64") as mock_ml:
        # Устанавливаем возвращаемые значения при вызове Celery tasks
        mock_ml.return_value = Mock(id="resize_task_id")