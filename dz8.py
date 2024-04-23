import sqlite3


def create_connection(hw_bd):
    conn = None
    try:
        conn = sqlite3.connect(hw_bd)
    except sqlite3.Error as e:
        print(e)
    return conn


def create_table(connection, sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
    except sqlite3.Error as e:
        print(e)


sql_countries_table = '''
CREATE TABLE countries (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    title VARCHAR(200) NOT NULL
)
'''

sql_cities_table = '''
CREATE TABLE cities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    area REAL DEFAULT 0,
    country_id INTEGER,
    FOREIGN KEY(country_id) REFERENCES countries(id)
)
'''

sql_students_table = '''
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    city_id INTEGER,
    FOREIGN KEY(city_id) REFERENCES cities(id)
)
'''


def insert_countries(connection, countries):
    try:
        sql = '''INSERT INTO countries
                 (title)
                 VALUES (?)
              '''
        cursor = connection.cursor()
        cursor.execute(sql, countries)
        connection.commit()
    except sqlite3.Error as e:
        print(e)


def insert_cities(connection, cities):
    try:
        sql = '''INSERT INTO cities
                 (title, area, country_id)
                 VALUES (?, ?, ?)
              '''
        cursor = connection.cursor()
        cursor.execute(sql, cities)
        connection.commit()
    except sqlite3.Error as e:
        print(e)


def insert_students(connection, students):
    try:
        sql = '''INSERT INTO students
                 (first_name, last_name, city_id)
                 VALUES (?, ?, ?)
                 '''
        cursor = connection.cursor()
        cursor.execute(sql, students)
        connection.commit()
    except sqlite3.Error as e:
        print(e)


my_connection = create_connection("hw.db")
if my_connection:
    print("Successfully connected to database")

# Создание трех таблиц

create_table(my_connection, sql_countries_table)
create_table(my_connection, sql_cities_table)
create_table(my_connection, sql_students_table)

# Создание стран

insert_countries(my_connection, ('Japan',))
insert_countries(my_connection, ('China',))
insert_countries(my_connection, ('Korea',))

# Создание городов

insert_cities(my_connection, ('Tokyo', 2194, 2))
insert_cities(my_connection, ('Nagasaki', 405.9, 3))
insert_cities(my_connection, ('Hiroshima', 906.7, 1))
insert_cities(my_connection, ('Pekin', 16411, 2))
insert_cities(my_connection, ('Shanghai', 6340, 3))
insert_cities(my_connection, ('Hong Kong', 2755, 1))
insert_cities(my_connection, ('Seoul', 605.2, 2))

# Создание студентов

insert_students(my_connection, ('Zhong', 'Xina', 1))
insert_students(my_connection, ('Don', 'Simon', 2))
insert_students(my_connection, ('Alexandr', 'Zubarev', 1))
insert_students(my_connection, ('Pavel', 'The Container', 2))
insert_students(my_connection, ('Sasha', 'Shlyapik', 3))
insert_students(my_connection, ('Niko', 'Glai', 4))
insert_students(my_connection, ('The', 'Wock', 3))
insert_students(my_connection, ('Fedor', 'Ivanov', 5))
insert_students(my_connection, ('Michel', 'Jackson', 6))
insert_students(my_connection, ('Vanyka', 'The silverhand', 4))
insert_students(my_connection, ('Fredy', 'Fasber', 7))
insert_students(my_connection, ('Mr', 'Beast', 6))
insert_students(my_connection, ('Coral', 'Grims', 1))
insert_students(my_connection, ('Waltuh', 'Waltuh', 6))
insert_students(my_connection, ('Rick', 'Grims', 1))


def get_cities(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title FROM cities")
        cities = cursor.fetchall()
        return cities
    except sqlite3.Error as e:
        print(e)
        return []


def get_students_by_city_id(conn, city_id):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT students.first_name, students.last_name, countries.title, cities.title, cities.area "
                       "FROM students "
                       "JOIN cities ON students.city_id = cities.id "
                       "JOIN countries ON cities.country_id = countries.id "
                       "WHERE cities.id = ?", (city_id,))
        students = cursor.fetchall()
        return students
    except sqlite3.Error as e:
        print(e)
        return []


def main():
    conn = create_connection("hw.db")
    if not conn:
        print("Ошибка подключения к базе данных.")
        return

    print(
        "Вы можете отобразить список учеников по выбранному id города из перечня городов ниже, для выхода из программы введите 0:\n")

    cities = get_cities(conn)
    if not cities:
        print("Ошибка при получении списка городов.")
        conn.close()
        return

    for city in cities:
        print(f"{city[0]}. {city[1]}")

    while True:
        city_id = input("\nВведите id города (для выхода введите 0): ")

        if city_id == '0':
            break

        try:
            city_id = int(city_id)
            if city_id < 0 or city_id > len(cities):
                print("Неверный id города. Пожалуйста, введите id из списка.")
                continue
        except ValueError:
            print("Неверный формат id города. Пожалуйста, введите целое число.")
            continue

        students = get_students_by_city_id(conn, city_id)

        if not students:
            print("В выбранном городе нет учеников.")
        else:
            print("\nУченики в выбранном городе:")
            for student in students:
                print(
                    f"Имя: {student[0]}, Фамилия: {student[1]}, Страна: {student[2]}, Город: {student[3]}, Площадь города: {student[4]}")

    conn.close()


if __name__ == "__main__":
    main()
