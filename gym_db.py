import sqlite3
import graf
import pickle

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

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                 member_id INTEGER,
                 bucks FLOAT,
                 tugric FLOAT,
                 chervonec FLOAT,
                 bondage FLOAT,
                 UNIQUE(member_id)
            )
            """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Tugrick (
             cost FLOAT
        )
        """)

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS Chervonec (
                 cost FLOAT
            )
            """)

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS Bondage (
                 cost FLOAT
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


class Economy:
    def __init__(self):
        pass

    def reg_player(self, player_id):
        cursor.execute(f"""
        INSERT INTO players VALUES
        ({player_id}, 300, 0, 0, 0)
        """)
        return True

    def get_money_info(self, player_id):
        cursor.execute(f"""
                SELECT bucks, tugric, chervonec, bondage FROM players WHERE member_id={player_id}
                """)
        money_inf = cursor.fetchone()
        if money_inf is None:
            self.reg_player(player_id)
            cursor.execute(f"""
                            SELECT bucks, tugric, chervonec, bondage FROM players WHERE member_id={player_id}
                            """)
            money_inf = cursor.fetchone()
        return money_inf

    def change_bucks(self, player_id, money):
        player_money = self.get_money_info(player_id)[0]
        cursor.execute(f"""
                        UPDATE players SET bucks={round(player_money + money, 8)} WHERE member_id={player_id}
                        """)
        connection.commit()
        return True

    def hour_bucks(self):
        cursor.execute(f"""
                        SELECT member_id, bucks FROM players
                        """)
        players = cursor.fetchall()
        for player in players:
            cursor.execute(f"""
                                    UPDATE players SET bucks={player[1] + 10} WHERE member_id={player[0]}
                                    """)
        connection.commit()

    def change_cherv(self, player_id, ammount):
        player_cherv = self.get_money_info(player_id)[2]
        cursor.execute(f"""
                                UPDATE players SET chervonec={round(player_cherv + ammount, 8)} WHERE member_id={player_id}
                                """)
        connection.commit()

    def change_tug(self, player_id, ammount):
        player_tug = self.get_money_info(player_id)[1]
        cursor.execute(f"""
                                UPDATE players SET tugric={round(player_tug + ammount, 8)} WHERE member_id={player_id}
                                """)
        connection.commit()

    def change_bondage(self, player_id, ammount):
        player_bondage = self.get_money_info(player_id)[3]
        cursor.execute(f"""
                                UPDATE players SET bondage={player_bondage + ammount} WHERE member_id={player_id}
                                """)
        connection.commit()

    def get_top_info(self):
        cursor.execute(f"""
                SELECT member_id, bucks, tugric, chervonec, bondage FROM players ORDER BY bucks DESC
                """)
        money_inf = cursor.fetchall()
        return money_inf

    def rand_currency(self):
        data = graf.generate_info()
        with open("currency", "wb")as file:
            pickle.dump(data, file)
        return True

    def update_currency(self):
        with open("currency", "rb")as file:
            data = pickle.load(file)
        graf.update_info(data[0], data[1], data[2])
        with open("currency", "wb")as file:
            pickle.dump(data, file)
        return True

    def get_currency_graf(self):
        with open("currency", "rb")as file:
            data = pickle.load(file)
        filename = "currency.png"
        graf.make_currency_graf(data1=data[0], data2=data[1], filename=filename)
        return filename

    def get_bondage_graf(self):
        with open("currency", "rb")as file:
            data = pickle.load(file)
        filename = "bonadge.png"
        graf.make_b_graf(data=data[2], filename=filename)
        return filename

    def get_currency(self):
        with open("currency", "rb")as file:
            data = pickle.load(file)
        return data