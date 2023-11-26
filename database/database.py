import sqlite3 as sq
from datetime import datetime

def sql_start():
    global base, cur
    base = sq.connect("SchoolBot.db")
    cur = base.cursor()
    if base:
        print("Database connected ok!")
    base.execute("CREATE TABLE IF NOT EXISTS userColumn(userID TEXT PRIMARY KEY, username TEXT, "
                 "name TEXT, lang TEXT, person TEXT, Class TEXT)"
                 )
    base.execute("CREATE TABLE IF NOT EXISTS userColumnAppeal(userID TEXT, time TEXT, person TEXT, "
                 "username TEXT, "
                 "name TEXT, Class TEXT, pscZdvr TEXT, cause TEXT, descriptionOfProblem TEXT, contact TEXT)"
                 )
    base.execute("CREATE TABLE IF NOT EXISTS userColumnConsultation(userID TEXT, time TEXT, person TEXT, "
                 "username TEXT, name TEXT, Class TEXT, pscZdvr TEXT, dayOfTheWeek TEXT, contact TEXT)"
                 )
    base.execute('CREATE TABLE IF NOT EXISTS adminId(admin_id)')
    base.commit()


def sql_read_admins():
    i = []
    for ret in cur.execute('SELECT * FROM adminId').fetchall():
        i.append(ret[0])

    return i


async def createUserColumn(userID, username, name, lang, person, Class):
    profile = cur.execute("SELECT 1 FROM userColumn WHERE userID == '{key}'".format(key=userID)).fetchone()
    if not profile:
        cur.execute("INSERT INTO userColumn (userID, username, name, lang, person, Class) VALUES(?, ?, ?, ?, ?, ?)", (userID, username,
                                                                                                             name, lang,
                                                                                                             person, Class))
        base.commit()


async def createUserColumnAppeal(userID, person, username, name, Class, pscZdvr, cause, descriptionOfProblem, contact):
    appeal = cur.execute("SELECT 1 FROM userColumnAppeal WHERE userID == '{key}'".format(key=userID)).fetchone()
    time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    cur.execute("INSERT INTO userColumnAppeal (userID, time, person, username, name, Class, pscZdvr, cause, "
                "descriptionOfProblem, contact) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (userID, time,
                                                                                        person, username,
                                                                                        name, Class,
                                                                                        pscZdvr, cause,
                                                                                        descriptionOfProblem,
                                                                                        contact))
    base.commit()


async def createUserColumnConsultation(userID, person, username, name, Class, pscZdvr, dayOfTheWeek, contact):
    consultation = cur.execute("SELECT 1 FROM userColumnConsultation WHERE userID == '{key}'".
                               format(key=userID)).fetchone()
    time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    cur.execute("INSERT INTO userColumnConsultation (userID, time, person, username, name, Class, pscZdvr, "
                "dayOfTheWeek, "
                "contact) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (userID, time,
                                                               person, username,
                                                               name, Class,
                                                               pscZdvr,
                                                               dayOfTheWeek,
                                                               contact))
    base.commit()


async def setNewLang(userID, newLang):
    lang = cur.execute("UPDATE userColumn SET lang = ? WHERE userID = ?", (newLang, userID))

    base.commit()


async def userExist(userID):
    user = cur.execute("SELECT 1 FROM userColumn WHERE userID == '{key}'".format(key=userID)).fetchone()

    if user:
        return True


async def getUserLang(userID):
    userLang = cur.execute("SELECT lang FROM userColumn WHERE userID = '{key}'".format(key=userID)).fetchone()

    return userLang[0]


async def getName(userID):
    name = cur.execute("SELECT name FROM userColumn WHERE userID = '{key}'".format(key=userID)).fetchone()

    return name[0]


async def getUserPerson(userID):
    userPerson = cur.execute("SELECT person FROM userColumn WHERE userID = '{key}'".format(key=userID)).fetchone()

    return userPerson[0]


async def getUserClass(userID):
    name = cur.execute("SELECT Class FROM userColumn WHERE userID = '{key}'".format(key=userID)).fetchone()

    return name[0]


async def sql_read_consultation() -> str:
    string = ""
    i = 0

    for ret in cur.execute('SELECT * FROM userColumnConsultation').fetchall():
        string += f"ID пользователя: <b>{ret[0]}\n</b>" \
                  f"Время подачи заявки: <b>{ret[1]}\n</b>" \
                  f"Кто подал заявку: <b>{ret[2]}\n</b>" \
                  f"Username: <b>{ret[3]}\n</b>" \
                  f"ФИО: <b>{ret[4]}\n</b>" \
                  f"Класс: <b>{ret[5]}\n</b>" \
                  f"К кому обращались: <b>{ret[6]}\n</b>" \
                  f"День недели: <b>{ret[7]}\n</b>" \
                  f"Контакты: <b>{ret[8]}\n\n</b>"
        i += 1

    string += f"Количество заявок: <b>{i}</b>"
    return string


async def sql_read_appeal() -> str:
    string = ""
    i = 0

    for ret in cur.execute('SELECT * FROM userColumnAppeal').fetchall():
        string += f"ID пользователя: <b>{ret[0]}\n</b>" \
                  f"Время подачи заявки: <b>{ret[1]}\n</b>" \
                  f"Кто подал заявку: <b>{ret[2]}\n</b>" \
                  f"Username: <b>{ret[3]}\n</b>" \
                  f"ФИО: <b>{ret[4]}\n</b>" \
                  f"Класс: <b>{ret[5]}\n</b>" \
                  f"К кому обращались: <b>{ret[6]}\n</b>" \
                  f"Причина: <b>{ret[7]}\n</b>" \
                  f"Описание проблемы: <b>{ret[8]}\n</b>" \
                  f"Контакты: <b>{ret[9]}</b>\n\n"
        i += 1

    string += f"Количество заявок: <b>{i}</b>"

    return string


async def sql_read_admins_for_admin():
    string = ""
    i = 0

    for ret in cur.execute('SELECT * FROM adminId').fetchall():
        string += f"ID: <b>{ret[0]}</b>\n\n"
        i += 1

    string += f"Количество админов: <b>{i}</b>"
    return string


async def sql_delete_column_query():
    cur.execute("DELETE FROM userColumnAppeal")
    cur.execute("DELETE FROM userColumnConsultation")

    base.commit()


async def sql_add_admins(admin_id):
    admin = cur.execute("SELECT 1 FROM adminId WHERE admin_id == '{key}'".format(key=admin_id)).fetchone()
    if not admin:
        cur.execute("INSERT INTO adminId (admin_id) VALUES (?)", (admin_id,))
        base.commit()