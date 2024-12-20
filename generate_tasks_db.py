import sqlite3
from faker import Faker

# Створення та підключення до бази даних SQLite
conn = sqlite3.connect('tasks_management.db')  # Створення бази даних у файлі
cursor = conn.cursor()

# Створення таблиці users з унікальним email
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);
''')

# Створення таблиці status з унікальним name
cursor.execute('''
CREATE TABLE IF NOT EXISTS status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL
);
''')

# Створення таблиці tasks з каскадним видаленням завдань при видаленні користувача
cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    status_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (status_id) REFERENCES status (id),
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);
''')

# Заповнення таблиці status
statuses = [('new',), ('in progress',), ('completed',)]
cursor.executemany('INSERT OR IGNORE INTO status (name) VALUES (?);', statuses)

# Використання Faker для генерації даних
fake = Faker()

# Генерація унікальних користувачів
unique_emails = set()
users = []

while len(unique_emails) < 5:
    email = fake.email()
    if email not in unique_emails:
        unique_emails.add(email)
        users.append((fake.name(), email))

cursor.executemany('INSERT OR IGNORE INTO users (fullname, email) VALUES (?, ?);', users)

# Генерація завдань
tasks = [
    (
        fake.sentence(nb_words=3),  # Назва завдання
        fake.text(max_nb_chars=200),  # Опис завдання
        fake.random_int(min=1, max=3),  # Статус (id)
        fake.random_int(min=1, max=len(users))  # Користувач (id)
    ) for _ in range(10)
]
cursor.executemany('INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?);', tasks)

# Збереження змін
conn.commit()

# Вивід даних для перевірки
print("Users:")
cursor.execute("SELECT * FROM users;")
print(cursor.fetchall())

print("\nStatus:")
cursor.execute("SELECT * FROM status;")
print(cursor.fetchall())

print("\nTasks:")
cursor.execute("SELECT * FROM tasks;")
print(cursor.fetchall())

# Закриття з'єднання
conn.close()
