#!/usr/bin/python
import os
import sqlite3
from sqlite3 import Error
import user_info as user
import datetime
import contact as ctct

db_file = "data.db"

create_users_sql = """CREATE TABLE `users` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`email`	TEXT,
	`displayname`	TEXT,
	`nickname`	TEXT,
	`avatar`	TEXTf
);"""

create_messsagestemplates_sql = """CREATE TABLE `messagestemplates` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`message`	BLOB
);"""

create_contacts_sql = """CREATE TABLE `contacts` (
	`id`	TEXT UNIQUE,
	`title`	TEXT,
	`selected`	TEXT,
	`type`	TEXT
);"""

create_logs_sql = """CREATE TABLE `logs` (
	`id`	INTEGER UNIQUE,
	`display`	BLOB,
	`sent_time`	TEXT,
	`message`	BLOB,
	`ids`	BLOB,
	PRIMARY KEY(`id`)
);"""


def create_connection():
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, db_file)
        conn = sqlite3.connect(db_path)
        return conn
    except Error as e:
        print(e)

    return None


def closecon(conn):
    conn.commit()
    conn.close()


def insert_user_info(user_info):
    try:
        conn = create_connection()
        sql = " INSERT INTO users(email,displayname,nickname,avatar) VALUES('{0}','{1}','{2}','{3}') ".format(
            user_info.email, user_info.displayname, user_info.nickname, user_info.avatar)
        cur = conn.cursor()

        cur.execute(sql)
        return cur.lastrowid
    except Exception as e:
        print(e)
    finally:
        closecon(conn)


def insert_contact(contact):
    try:
        conn = create_connection()
        sql = " INSERT INTO contacts(id,title,selected,type) VALUES('{0}','{1}','{2}','{3}') ".format(contact.id,
                                                                                                      contact.title,
                                                                                                      contact.selected,
                                                                                                      contact.type)
        cur = conn.cursor()

        cur.execute(sql)
        return cur.lastrowid
    except Exception as e:
        print(e)
    finally:
        closecon(conn)


def create_tables():
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute(create_users_sql)
        cur = conn.cursor()
        cur.execute(create_contacts_sql)
        cur = conn.cursor()
        cur.execute(create_logs_sql)
        cur = conn.cursor()
        cur.execute(create_messsagestemplates_sql)

    except Exception as e:
        print(e)
    finally:
        closecon(conn)


def select_user_info():
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users order by id asc limit 1")
        rows = cur.fetchall()
        for row in rows:
            current_user = user.user_info(id=row[0], email=row[1], displayname=row[2],
                                          nickname=row[3], avatar=row[4])
            return current_user
    except Exception as e:
        create_tables()
        print(e)
    finally:
        closecon(conn)


def select_all_contacts():
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("SELECT title,selected,type FROM contacts")
        rows = cur.fetchall()
        # all = []
        # for row in rows:
        #     current_user = ctct.contact(id=row[0], title=row[1], selected=row[2],
        #                                 type=row[3])
        #     all.append(current_user)
        return rows
    except Exception as e:
        print(e)
    finally:
        closecon(conn)


def select_groups_contacts():
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("SELECT title,selected,type FROM contacts where type='group'")
        rows = cur.fetchall()
        return rows
    except Exception as e:
        print(e)
    finally:
        closecon(conn)
    # all = []
    # for row in rows:
    #     current_user = ctct.contact(id=row[0], title=row[1], selected=row[2],
    #                                 type=row[3])
    #     all.append(current_user)


def get_all_msg_templates():
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM messagestemplates")
        rows = cur.fetchall()
        return rows
    except Exception as e:
        print(e)
    finally:
        closecon(conn)
    # all = []
    # for row in rows:
    #     current_user = ctct.contact(id=row[0], title=row[1], selected=row[2],
    #                                 type=row[3])
    #     all.append(current_user)


def save_template(message):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """
    try:
        conn = create_connection()
        sql = " INSERT INTO messagestemplates(message) VALUES('{0}') ".format(message)
        cur = conn.cursor()
        cur.execute(sql)
        return cur.lastrowid
    except Exception as e:
        print(e)
    finally:
        closecon(conn)


def update_text(id, message):
    try:
        conn = create_connection()
        sql = " UPDATE messagestemplates SET message='{0}' where id='{1}'".format(message, id)
        cur = conn.cursor()
        cur.execute(sql)
        return cur.lastrowid
    except Exception as e:
        print(e)
    finally:
        closecon(conn)


def get_id_by_contact_name(contact_name):
    try:
        conn = create_connection()
        sql = "SELECT id FROM contacts where title='{0}'".format(contact_name)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return rows
    except Exception as e:
        print(e)
    finally:
        closecon(conn)
    # all = []
    # for row in rows:
    #     current_user = ctct.contact(id=row[0], title=row[1], selected=row[2],
    #                                 type=row[3])
    #     all.append(current_user)


def insert_log(ids, message):
    # message = message.replace("\n", "<br>")
    contactsstr = ""
    idsstr = ""
    i = 0
    for id in ids:
        name = get_contact_name_from_id(id)
        if i == len(ids) - 1:
            contactsstr += name[0][0]
            idsstr += id
        else:
            contactsstr += name[0][0] + ", "
            idsstr += id + ", "
        i += 1
    date = datetime.datetime.now()
    # print(contactsstr)
    # print(idsstr)
    try:
        conn = create_connection()
        sql = " INSERT INTO logs(display,sent_time,ids,message) VALUES('{0}','{1}','{2}','{3}') ".format(contactsstr,
                                                                                                         date, idsstr,
                                                                                                         message)
        cur = conn.cursor()
        cur.execute(sql)
        return cur.lastrowid
    except Exception as e:
        print(e)
    finally:
        closecon(conn)


def get_contact_name_from_id(id):
    try:
        conn = create_connection()
        sql = "SELECT title FROM contacts where id='{0}'".format(id)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return rows
    except Exception as e:
        print(e)
    finally:
        closecon(conn)


def update_contact_selected(ids):
    try:
        conn = create_connection()
        sql = " UPDATE contacts SET selected='no'"
        cur = conn.cursor()
        cur.execute(sql)
        for id in ids:
            sql = " UPDATE contacts SET selected='yes' where id='{0}'".format(id)
            cur = conn.cursor()
            cur.execute(sql)
        return cur.lastrowid
    except Exception as e:
        print(e)
    finally:
        closecon(conn)


def load_log():
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("SELECT display,sent_time,message FROM logs ORDER BY id desc LIMIT 20")
        rows = cur.fetchall()
        # all = []
        # for row in rows:
        #     current_user = ctct.contact(id=row[0], title=row[1], selected=row[2],
        #                                 type=row[3])
        #     all.append(current_user)
        return rows
    except Exception as e:
        print(e)
    finally:
        closecon(conn)


def clear_all_users():
    try:
        conn = create_connection()
        sql = " DELETE FROM users"
        cur = conn.cursor()
        cur.execute(sql)
        return cur.lastrowid
    except Exception as e:
        print(e)
    finally:
        closecon(conn)


def updatetable(messageid, message):
    try:
        conn = create_connection()
        sql = " UPDATE main.logs SET message='{0}' where id='{1}'".format(message, messageid)
        cur = conn.cursor()
        cur.execute(sql)
        return cur.lastrowid
    except Exception as e:
        print(e)
    finally:
        closecon(conn)


def clear_all_logs():
    try:
        conn = create_connection()
        sql = " DELETE FROM logs"
        cur = conn.cursor()
        cur.execute(sql)
        return cur.lastrowid
    except Exception as e:
        print(e)
    finally:
        closecon(conn)


def clear_all_contacts():
    try:
        conn = create_connection()
        sql = " DELETE FROM contacts"
        cur = conn.cursor()
        cur.execute(sql)
        return cur.lastrowid
    except Exception as e:
        print(e)
    finally:
        closecon(conn)


def clear_all_msgtemplates():
    try:
        conn = create_connection()
        sql = " DELETE FROM messagestemplates"
        cur = conn.cursor()
        cur.execute(sql)
        return cur.lastrowid
    except Exception as e:
        print(e)
    finally:
        closecon(conn)