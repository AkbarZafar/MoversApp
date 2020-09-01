import sqlite3


class Schema:
  def __init__(self):
    self.conn = sqlite3.connect('Movers.db')
    self.create_user_table()
    self.create_boxes_table()
    # Why are we calling user table before to_do table
    # what happens if we swap them?

  def create_boxes_table(self):
    query = """
    CREATE TABLE IF NOT EXISTS "Boxes" (
      id INTEGER PRIMARY KEY,
      Title TEXT NOT NULL,
      Description TEXT,
      UserId INTEGER FOREIGNKEY REFERENCES Users(id),
      is_deleted boolean default False
    );
    """

    self.conn.execute(query)

  def create_user_table(self):
    query = """
    CREATE TABLE IF NOT EXISTS "Users" (
      id INTEGER PRIMARY KEY,
      Name TEXT NOT NULL,
      Password TEXT NOT NULL
    );
    """
    self.conn.execute(query)


class BoxesModel:
  TABLENAME = "Boxes"

  def __init__(self):
    self.conn = sqlite3.connect('Movers.db')

  def create(self, text, description, UserId):
    query = f'insert into Boxes (Title, Description, UserId) values' \
            f'("{text}", "{description}", {UserId});'

    result = self.conn.execute(query)
    return result

  def select(self, UserId):
    query = f'select id, Title, Description ' \
            f'from Boxes where is_deleted = false and userId = {UserId}'

    result = self.conn.execute(query)
    return result

  def delete(self, id):
    query = f'update Boxes set is_deleted = true ' \
            f'where UserId = {id}'
    result = self.conn.execute(query)
    return result


