# =============================================================================
# exemplo_de_uso.py — script de teste do handout de persistência
# Rodar: python exemplo_de_uso.py → imprime todas as notas salvas no banco.db
# Útil para conferir o que está no banco sem abrir o servidor.
# 📖 README_1A.md → Parte 2 → "Pegadinhas e dicas"
# =============================================================================
from database import Database

db = Database('banco')

notes = db.get_all()
for note in notes:
    print(f'Anotação {note.id}:\n  Título: {note.title}\n  Conteúdo: {note.content}\n')
