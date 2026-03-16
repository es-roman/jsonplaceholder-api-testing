"""
Тесты для работы с постами JSONPlaceholder API.
"""

import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

# ------------ Позитивные тесты ------------ 

def test_get_all_posts_status_200():
    response = requests.get(f"{BASE_URL}/posts")
    assert response.status_code == 200 # Тест проверяет получение списка всех постов
    assert len(response.json()) == 100  # Тест проверяет получение в ответе ровно 100 постов

def test_get_single_post_by_id():
    response = requests.get(f"{BASE_URL}/posts/1")
    assert response.status_code == 200 # Тест проверяет получение одного поста по его ID
    data = response.json()
    assert data["id"] == 1 # Тест проверяет, что полученный id совпадает с запрошенным (1)
    assert "title" in data and "body" in data # Тест проверяет корректную структуру поста.
    Ожидается:
    - статус код 200
    - в ответе поле id совпадает с запрошенным (1)
    - присутствуют поля title и body (пост имеет корректную структуру)

def test_create_post_201():
    payload = {"title": "Новый пост", "body": "Тестовое тело поста", "userId": 1}
    response = requests.post(f"{BASE_URL}/posts", json=payload)
    assert response.status_code == 201 # Тест проверяет, что новый пост создан
    assert response.json()["title"] == "Новый пост" # Тест проверяет, что возвращается созданный пост с тем же заголовком, который отправляли 

def test_update_post_put_200():
    payload = {"id": 1, "title": "Обновлённый заголовок", "body": "Новое тело", "userId": 1}
    response = requests.put(f"{BASE_URL}/posts/1", json=payload)
    assert response.status_code == 200 # Тест проверяет, что пост обновился
    assert response.json()["title"] == "Обновлённый заголовок" # Тест проверяет, что в ответе возвращается обновлённый пост с новым заголовком

def test_update_post_patch_200():
    payload = {"title": "Только заголовок обновлён"}
    response = requests.patch(f"{BASE_URL}/posts/1", json=payload)
    assert response.status_code == 200 # Тест проверяет, что пост частично обновился
    assert response.json()["title"] == "Только заголовок обновлён" # Тест проверяет, что в ответе возвращается обновлённый пост с новым заголовком, остальные поля не изменяются

def test_delete_post_200():
    response = requests.delete(f"{BASE_URL}/posts/1")
    assert response.status_code == 200 # Тест проверяет удаление поста

# ------------ Параметризованные тесты ------------

@pytest.mark.parametrize("post_id", [5, 42, 77, 100])
def test_get_post_by_different_ids(post_id):
    response = requests.get(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == 200
    assert response.json()["id"] == post_id # Тест проверяет, что для четырёх разных номеров постов API возвращает правильный пост и не выдаёт ошибок

@pytest.mark.parametrize("comment_post_id", [1, 3, 10])
def test_get_comments_for_post(comment_post_id):
    response = requests.get(f"{BASE_URL}/posts/{comment_post_id}/comments")
    assert response.status_code == 200
    assert len(response.json()) > 0 # Тест проверяет, что список не пустой (длина поста точно больше нуля)

# ------------ Негативные тесты ------------ 

def test_get_non_existent_post_404():
    response = requests.get(f"{BASE_URL}/posts/99999")
    assert response.status_code == 404 # Тест проверяет, что поста с id = 99999 не существует

def test_create_post_empty_title():
    payload = {"title": "", "body": "тело", "userId": 1}
    response = requests.post(f"{BASE_URL}/posts", json=payload)
    assert response.status_code == 201 # Тест проверяет, примет ли API такой пост 

def test_create_post_invalid_user_id():
    payload = {"title": "тест", "body": "тест", "userId": "не_число"}
    response = requests.post(f"{BASE_URL}/posts", json=payload)
    assert response.status_code == 201 # Тест проверяет, примет ли API такой пост c некоректныv userId (ожидалось число)

@pytest.mark.parametrize("invalid_id", [0, -1, "string", 99999])
def test_get_post_invalid_id(invalid_id):
    response = requests.get(f"{BASE_URL}/posts/{invalid_id}")
    assert response.status_code in [404, 200] # Тест проверяет, что сервер не падает с внутренней ошибкой

def test_delete_non_existent_post():
    response = requests.delete(f"{BASE_URL}/posts/99999")
    assert response.status_code == 200 # Тест проверяет, что пост с номером 99999 удалился (ожидался ответ 404, но из-за особенностей API, статус - 200)
