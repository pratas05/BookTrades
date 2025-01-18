import sqlite3

def init_db():
    conexion = sqlite3.connect('book_trade.db')
    cursor = conexion.cursor()

    # Tabela de usuários
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Tabela de livros
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            genre TEXT NOT NULL,
            image_url TEXT NOT NULL,
            dateAdded TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Tabela de desejos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS wishlist (
        id TEXT PRIMARY KEY,              
        book_id TEXT NOT NULL,            
        user_id TEXT NOT NULL,            
        status TEXT NOT NULL,            
        FOREIGN KEY (book_id) REFERENCES books (id),  
        FOREIGN KEY (user_id) REFERENCES users (id)   
    )
    ''')

    # Tabela de trocas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tradelist (
        id TEXT PRIMARY KEY,              
        book_id TEXT NOT NULL,            
        user_id TEXT NOT NULL,            
        status TEXT NOT NULL,            
        FOREIGN KEY (book_id) REFERENCES books (id),  
        FOREIGN KEY (user_id) REFERENCES users (id)   
    )
    ''')

    #Tabela para ofertas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS offer (
        id TEXT PRIMARY KEY,
        bookA_id TEXT NOT NULL,
        userA_id TEXT NOT NULL,
        bookB_id TEXT NOT NULL,
        userB_id TEXT NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (bookA_id) REFERENCES books (id),
        FOREIGN KEY (userA_id) REFERENCES users (id),
        FOREIGN KEY (bookB_id) REFERENCES books (id),
        FOREIGN KEY (userB_id) REFERENCES users (id)
    )
    ''')
    conexion.commit()
    conexion.close()