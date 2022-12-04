import sqlite3

conn = sqlite3.connect('school.db')
cur = conn.cursor()
cur.execute('''
            CREATE TABLE IF NOT EXISTS teachers
             (t_id INT PRIMARY KEY,
             t_name TEXT,
             tg_id INT);''')
conn.commit()
cur.execute('''
            CREATE TABLE IF NOT EXISTS tasks
             (task_id INT PRIMARY KEY,
             teacher_id INT,
             task_type INT,
             task_text TEXT,
             task_date DATETIME,
             task_date_end DATETIME,
             task_status INT
             );''')
#task_type - 0 - открыть доступ, 1 - другое
#task_status - 0 - направлено, 1 - в работе, 2 - одобрено ОС, 3 - закрыто
conn.commit()

cur.execute('SELECT * FROM tasks')
for x in cur.fetchall():
    print(x)
cur.close()
conn.close()
#[(0, 'Вася', 1685023830), (1, 'Петя', 527995685)]