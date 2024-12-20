import sqlite3

# Створення бази даних і таблиць
def setup_database():
    conn = sqlite3.connect('tasks_management.db')
    cursor = conn.cursor()

    # Створення таблиці users
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL
    );
    ''')

    # Створення таблиці status
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS status (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(50) UNIQUE NOT NULL
    );
    ''')

    # Створення таблиці tasks
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(100) NOT NULL,
        description TEXT,
        status_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (status_id) REFERENCES status (id),
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    ''')

    # Заповнення таблиці status
    statuses = [('new',), ('in progress',), ('completed',)]
    cursor.executemany('INSERT OR IGNORE INTO status (name) VALUES (?);', statuses)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
    print("База даних створена та початкові дані додано.")
