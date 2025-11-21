from app import create_app, db
from app.models import User, MoodEntry

app = create_app()

with app.app_context():
    # Создаем все таблицы
    db.create_all()
    print("✅ Таблицы успешно созданы!")

    # Проверяем создание пользователя
    test_user = User(username='testuser', email='test@example.com')
    test_user.set_password('password123')

    # Проверяем создание записи настроения
    test_mood = MoodEntry(mood='happy', notes='Тестовая запись', user_id=1)

    print("✅ Модели работают корректно!")