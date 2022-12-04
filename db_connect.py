import sqlite3, smtplib
from datetime import datetime, timedelta


async def db_start():
    global conn, cur, adm
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
                 task_status INT DEFAULT 0
                 );''')
    # task_type - 0 - открыть доступ, 1 - другое
    # task_status - 0 - направлено, 1 - в работе, 2 - одобрено ОС, 3 - закрыто
    conn.commit()


def send_email():
    pass
    '''HOST = "mySMTP.server.com"
    SUBJECT = "Заявка по ЭЖД"
    TO = "trunov.dn@nika-school.ru"
    FROM = "python@mydomain.com"
    text = "Python 3.4 rules them all!"

    BODY = "\r\n".join((
        "From: %s" % FROM,
        "To: %s" % TO,
        "Subject: %s" % SUBJECT,
        "",
        text
    ))

    server = smtplib.SMTP(HOST)
    server.sendmail(FROM, [TO], BODY)
    server.quit()'''

def adm():
    global cur
    return cur.execute("SELECT tg_id FROM teachers WHERE t_id=?;", (1,)).fetchone()[0]


def check_last_t(id):
    global cur
    user = cur.execute("SELECT tg_id FROM teachers WHERE tg_id=?;", (id,))
    return user.fetchone()


def get_t(id):
    global cur
    user = cur.execute("SELECT t_id, t_name FROM teachers WHERE tg_id=?;", (id,))
    return user.fetchone()


async def new_t(id, name, tid):
    last_user = cur.execute("SELECT t_id FROM teachers ORDER BY t_id DESC LIMIT 1;").fetchall()
    if not last_user:
        uid = 0
    else:
        uid = last_user[0][0] + 1
    cur.execute("INSERT INTO teachers (t_id, t_name, tg_id) VALUES (?, ?, ?)", (uid, name, tid))
    conn.commit()

#запись заявки в БД
async def save_task(t, t_type, text):
    last_task = cur.execute("SELECT task_id FROM tasks ORDER BY task_id DESC LIMIT 1;").fetchall()
    if not last_task:
        tid = 0
    else:
        tid = last_task[0][0] + 1
    #получаем даты
    d = datetime.now()
    d1 = d + timedelta(days=2)
    cur.execute('''INSERT INTO tasks 
                (task_id, teacher_id, task_type, task_text, task_date, task_date_end, task_status)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''', (tid, t, t_type, text, d, d1, 0))
    conn.commit()
    return tid

#одобрение заявки
async def confirm_task(t):

    cur.execute('UPDATE tasks SET task_status=? WHERE task_id=?;', (2, t))
    conn.commit()