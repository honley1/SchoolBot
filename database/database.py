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
                 "username TEXT, name TEXT, Class TEXT, pscZdvr TEXT, dayOfTheWeek TEXT, contact TEXT)")
    base.commit()


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
