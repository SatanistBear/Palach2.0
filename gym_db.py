import sqlite3


def init():
    global cursor, connection
    connection = sqlite3.connect('gym.db')
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS condom_facts (
        id INTEGER,
        fact TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS condom_count (
        member_id INTEGER,
        count INTEGER
    )
    """)


def w_fact(id, fact):
    cursor.execute(f"""
    INSERT INTO condom_facts VALUES
    ({id}, '{fact}')
    """)
    connection.commit()
    return True


def r_fact(id):
    cursor.execute(f"""
    SELECT fact FROM condom_facts WHERE id = {id} 
    """)
    fact = cursor.fetchone()
    return fact


def del_fact(id):
    cursor.execute(f"""
    DELETE FROM condom_facts WHERE id = {id}
    """)
    return True


def add_member(member_id):
    cursor.execute(f"""
    INSERT INTO condom_count VALUES
    ({member_id}, 1)
    """)
    connection.commit()
    return True


def add_condom(member_id):
    cursor.execute(f"""
    SELECT count FROM condom_count WHERE member_id={member_id}
    """)
    c = cursor.fetchone()[0]
    cursor.execute(f"""
        UPDATE condom_count SET count = {c + 1} WHERE member_id = {member_id}
        """)
    connection.commit()
    return True


def get_condoms(member_id):
    cursor.execute(f"""
        SELECT count FROM condom_count WHERE member_id={member_id}
        """)
    count = cursor.fetchone()
    if count is not None:
        count = count[0]
    return count


def get_all_condoms():
    cursor.execute(f"""
        SELECT member_id,count FROM condom_count
        """)
    count = cursor.fetchall()
    return count




