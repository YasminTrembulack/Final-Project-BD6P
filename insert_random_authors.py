import random
import mysql.connector
from faker import Faker
from config import db_config

# Configurações do banco
db = mysql.connector.connect(**db_config)

cursor = db.cursor()

fake_pt = Faker('pt_BR')  # nomes brasileiros
fake_en = Faker('en_US')  # nomes americanos/ingleses

authors = []

for _ in range(50):
    # Escolhe aleatoriamente PT ou EN
    if random.choice([True, False]):
        authors.append(fake_pt.name())
    else:
        authors.append(fake_en.name())

print("Autores gerados:", authors)

# 2️⃣ Buscar todos os livros
cursor.execute("SELECT id FROM books;")
books = cursor.fetchall()  # lista de tuplas [(1,), (2,), ...]

# 3️⃣ Atualizar cada livro com um autor aleatório
for book in books:
    book_id = book[0]
    random_author = random.choice(authors)
    cursor.execute(
        "UPDATE books SET author = %s WHERE id = %s;",
        (random_author, book_id)
    )

db.commit()
cursor.close()
db.close()

print("Autores inseridos aleatoriamente nos livros!")
