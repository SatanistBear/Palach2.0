import sqlite3


def init():
    global cursor, connection
    connection = sqlite3.connect('gym.db')
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS condom_facts (
        id INTEGER,
        fact TEXT,
        UNIQUE(fact)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS condom_count (
        member_id INTEGER,
        count INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ranks (
        rank TEXT,
        condoms INTEGER
    )
    """)


class Facts:
    def __init__(self):
        pass

    def facts_max_id(self):
        cursor.execute("""
                SELECT MAX(id) FROM condom_facts
                """)
        num = cursor.fetchall()[0][0]
        if num is None:
            num = 0
        return num

    def w_fact(self, fact):
        cursor.execute(f"""
        INSERT OR IGNORE INTO condom_facts VALUES
        ({Facts.facts_max_id(self) + 1}, "{fact}")
        """)
        connection.commit()
        return True

    def r_fact(self, id):
        cursor.execute(f"""
        SELECT fact FROM condom_facts WHERE id = {id} 
        """)
        fact = cursor.fetchone()[0]
        return fact

    def del_fact(self, id):
        cursor.execute(f"""
        DELETE FROM condom_facts WHERE id = {id}
        """)
        connection.commit()
        return True

    def all_facts(self):
        cursor.execute("""
        SELECT * FROM condom_facts
        """)
        return cursor.fetchall()


class Condoms:
    def __init__(self):
        pass

    def add_member(self, member_id):
        cursor.execute(f"""
        INSERT INTO condom_count VALUES
        ({member_id}, 1)
        """)
        connection.commit()
        return True

    def del_fact(self, member_id):
        cursor.execute(f"""
        DELETE FROM condom_count WHERE member_id = {member_id}
        """)
        connection.commit()
        return True

    def add_condom(self, member_id):
        cursor.execute(f"""
        SELECT count FROM condom_count WHERE member_id={member_id}
        """)
        count = cursor.fetchone()[0]
        cursor.execute(f"""
            UPDATE condom_count SET count = {count + 1} WHERE member_id = {member_id}
            """)
        connection.commit()
        return True

    def get_condoms(self, member_id):
        cursor.execute(f"""
            SELECT count FROM condom_count WHERE member_id={member_id}
            """)
        count = cursor.fetchone()
        if count is not None:
            count = count[0]
        return count

    def get_all_condoms(self):
        cursor.execute(f"""
            SELECT * FROM condom_count
            """)
        count = cursor.fetchall()
        return count








