import sqlite3

# 1. Подключение к БД библиотеки
connection = sqlite3.connect('digital_library.db')
cursor = connection.cursor()

# Включаем поддержку внешних ключей
cursor.execute("PRAGMA foreign_keys = ON")

# 2. Удаление старых таблиц
cursor.execute("DROP TABLE IF EXISTS borrowings")
cursor.execute("DROP TABLE IF EXISTS books")
cursor.execute("DROP TABLE IF EXISTS readers")

# 3. Создание таблицы читателей (Readers)
cursor.execute("""
CREATE TABLE readers (
    reader_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    library_card TEXT,
    preferred_genre TEXT DEFAULT 'Классика',
    registered_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

# 4. Создание таблицы книг (Books)
cursor.execute("""
CREATE TABLE books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    isbn TEXT,
    rental_price REAL NOT NULL,
    copies_available INTEGER DEFAULT 1,
    is_digital BOOLEAN DEFAULT 1
)
""")

# 5. Создание таблицы выдачи (Borrowing)
cursor.execute("""
CREATE TABLE borrowings (
    borrow_id INTEGER PRIMARY KEY AUTOINCREMENT,
    reader_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    issue_date TEXT NOT NULL,
    return_deadline TEXT,
    deposit_amount REAL,
    status TEXT CHECK(status IN ('new', 'shipped', 'delivered', 'cancelled')), -- Сохранено по структуре (взято, в пути, возвращено, отменено)
    FOREIGN KEY (reader_id) REFERENCES readers(reader_id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE SET NULL
)
""")

# 6. Данные читателей
readers_data = [
    ("Иван Петров", "ivan.petrov@mail.ru", "BC-001", "Научпоп", "2024-01-15"),
    ("Мария Смирнова", "maria.smirnova@yandex.ru", "BC-002", "Детектив", "2024-02-20"),
    ("Алексей Козлов", "alex.kozlov@gmail.com", "BC-003", "Фантастика", "2024-03-10"),
    ("Елена Морозова", "elena.morozova@mail.ru", "BC-004", "Роман", "2024-03-25"),
    ("Дмитрий Волков", "dmitry.volkov@yandex.ru", "BC-005", "История", "2024-04-05"),
    ("Ольга Лебедева", "olga.lebedeva@gmail.com", "BC-006", "Психология", "2024-04-18"),
    ("Сергей Соколов", "sergey.sokolov@mail.ru", "BC-007", "Классика", "2024-05-02"),
    ("Анна Кузнецова", "anna.kuznetsova@yandex.ru", "BC-008", "Ужасы", "2024-05-20"),
    ("Максим Попов", "maxim.popov@gmail.com", "BC-009", "Фэнтези", "2024-06-08"),
    ("Наталья Васильева", "natalya.vasilieva@mail.ru", "BC-010", "Детектив", "2024-06-25"),
    ("Андрей Михайлов", "andrey.mikhailov@yandex.ru", "BC-011", "Наука", "2024-07-10"),
    ("Екатерина Новикова", "ekaterina.novikova@gmail.com", "BC-012", "Биография", "2024-07-28"),
    ("Павел Федоров", "pavel.fedorov@mail.ru", "BC-013", "Классика", "2024-08-15"),
    ("Юлия Романова", "yulia.romanova@yandex.ru", "BC-014", "Поэзия", "2024-09-01"),
    ("Николай Григорьев", "nikolay.grigoriev@gmail.com", "BC-015", "Триллер", "2024-09-20")
]

# 7. Вставка данных 
cursor.executemany("""
INSERT INTO readers (full_name, email, library_card, preferred_genre, registered_at) 
VALUES (?, ?, ?, ?, ?)
""", readers_data)

connection.commit()
print("База данных онлайн-библиотеки успешно создана.")

# 8. Закрытие
connection.close()
