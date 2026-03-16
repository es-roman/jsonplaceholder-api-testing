# jsonplaceholder-api-testing
API-тестирование JSONPlaceholder

Pet-проект для позиции QA-тестировщика

# Что сделано:
- 18 автотестов на Python + pytest + requests
- Покрытие CRUD-операций (`/posts` и `/comments`)
- Валидация статус-кодов (200, 201, 404)
- Негативные сценарии и техники тест-дизайна:
  - классы эквивалентности
  - граничные значения
  - неверные типы данных
- Настроен **CI/CD** через GitHub Actions (тесты запускаются автоматически при каждом push)

### Как запустить локально:
```bash
pip install -r requirements.txt
pytest tests/ -v --html=report.html
