import sqlite3

# Підключення до бази даних
conn = sqlite3.connect('tasks_management.db')
cursor = conn.cursor()

# Виконання SQL-запитів

# 1. Отримати всі завдання певного користувача
user_id = 1
cursor.execute("SELECT * FROM tasks WHERE user_id = ?;", (user_id,))
tasks_by_user = cursor.fetchall()
print("1. Завдання певного користувача:")
print(tasks_by_user)

# 2. Вибрати завдання за певним статусом
status_name = 'new'
cursor.execute("""
SELECT * FROM tasks 
WHERE status_id = (SELECT id FROM status WHERE name = ?);
""", (status_name,))
tasks_by_status = cursor.fetchall()
print("\n2. Завдання за статусом 'new':")
print(tasks_by_status)

# 3. Оновити статус конкретного завдання
task_id = 1
new_status_name = 'in progress'
cursor.execute("""
UPDATE tasks
SET status_id = (SELECT id FROM status WHERE name = ?)
WHERE id = ?;
""", (new_status_name, task_id))
conn.commit()
print("\n3. Статус завдання оновлено.")

# 4. Отримати список користувачів, які не мають жодного завдання
cursor.execute("""
SELECT * FROM users
WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks);
""")
users_without_tasks = cursor.fetchall()
print("\n4. Користувачі без завдань:")
print(users_without_tasks)

# 5. Додати нове завдання для конкретного користувача
new_task = ('Новий заголовок', 'Опис нового завдання', 1, 1)
cursor.execute("""
INSERT INTO tasks (title, description, status_id, user_id)
VALUES (?, ?, ?, ?);
""", new_task)
conn.commit()
print("\n5. Нове завдання додано.")

# 6. Отримати всі завдання, які ще не завершено
cursor.execute("""
SELECT * FROM tasks
WHERE status_id != (SELECT id FROM status WHERE name = 'completed');
""")
incomplete_tasks = cursor.fetchall()
print("\n6. Незавершені завдання:")
print(incomplete_tasks)

# 7. Видалити конкретне завдання
task_id_to_delete = 2
cursor.execute("DELETE FROM tasks WHERE id = ?;", (task_id_to_delete,))
conn.commit()
print("\n7. Завдання видалено.")

# 8. Знайти користувачів з певною електронною поштою
email_pattern = '%@gmail.com'
cursor.execute("SELECT * FROM users WHERE email LIKE ?;", (email_pattern,))
users_with_email_pattern = cursor.fetchall()
print("\n8. Користувачі з електронною поштою '@gmail.com':")
print(users_with_email_pattern)

# 9. Оновити ім'я користувача
user_id_to_update = 1
new_fullname = 'Оновлене ім\'я'
cursor.execute("UPDATE users SET fullname = ? WHERE id = ?;", (new_fullname, user_id_to_update))
conn.commit()
print("\n9. Ім'я користувача оновлено.")

# 10. Отримати кількість завдань для кожного статусу
cursor.execute("""
SELECT status.name, COUNT(tasks.id) AS task_count
FROM status
LEFT JOIN tasks ON status.id = tasks.status_id
GROUP BY status.id;
""")
task_count_by_status = cursor.fetchall()
print("\n10. Кількість завдань за статусами:")
print(task_count_by_status)

# Закриття підключення
conn.close()
