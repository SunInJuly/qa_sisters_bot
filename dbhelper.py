import sqlite3

from utils import Opening


class DBHelper:
    def __init__(self, dbname="sisters.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS openings (description text, contact text)"
        self.conn.execute(stmt)
        self.conn.commit()

    def add_message(self, message_text, contact):
        stmt = "INSERT INTO openings VALUES (?,?)"
        args = (message_text, contact)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, item_text):
        stmt = "DELETE FROM openings WHERE description = (?)"
        args = (item_text, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self):
        stmt = "SELECT description, contact FROM openings"
        return [Opening(contact=x[1], description=x[0]) for x in self.conn.execute(stmt)]