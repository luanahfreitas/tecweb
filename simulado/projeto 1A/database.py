import sqlite3
from dataclasses import dataclass

@dataclass
class Note:
    id: int = None
    title: str = None
    content: str = ''
    favorite: bool = False

class Database:
    def __init__(self,nome):
        self.conn = sqlite3.connect(nome + '.db')
        self.conn.execute("CREATE TABLE IF NOT EXISTS note (id INTEGER PRIMARY KEY, title TEXT, content TEXT NOT NULL, favorite INTEGER DEFAULT 0);")

    def add(self,note):
        self.conn.execute("INSERT INTO note (title, content) VALUES ('" + note.title + "', '" + note.content + "');")
        self.conn.commit()
    
    def get_all(self):
        notes = []
        cursor = self.conn.execute("SELECT id, title, content, favorite FROM note ORDER BY favorite DESC, id ASC")
        for linha in cursor:
            notes.append(Note(id=linha[0], title=linha[1], content=linha[2], favorite=bool(linha[3])))
        return notes

    def update(self, entry):
        self.conn.execute("UPDATE note SET title = '" + entry.title + "', content = '" + entry.content + "' WHERE id = " + str(entry.id) + ";")
        self.conn.commit()

    def delete(self, note_id):
        self.conn.execute("DELETE FROM note WHERE id = " + str(note_id) + ";")
        self.conn.commit()

    def get(self, note_id):
        cursor = self.conn.execute("SELECT id, title, content, favorite FROM note WHERE id = " + str(note_id) + ";")
        linha = cursor.fetchone()
        if linha is None:
            return None
        return Note(id=linha[0], title=linha[1], content=linha[2], favorite=bool(linha[3]))

    def toggle_favorite(self, note_id):
        nota = self.get(note_id)
        novo_valor = 0 if nota.favorite else 1
        self.conn.execute("UPDATE note SET favorite = " + str(novo_valor) + " WHERE id = " + str(note_id) + ";")
        self.conn.commit()


    