import sqlite3
import bcrypt
from flask import Flask, jsonify, render_template, redirect, session, url_for, flash, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import random
import string
from datetime import date
from database import init_db

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'book_trade_123'  # Substituir por uma chave secreta segura

# Flask Login Configuration
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Classe de modelo para o Flask-Login
class User(UserMixin):
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

# Função para inicializar a base de dados
init_db()

# Carregar utilizador para o Flask-Login
@login_manager.user_loader
def load_user(user_id):
    conexion = sqlite3.connect('book_trade.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conexion.close()

    if user:
        return User(id=user[0], name=user[1], email=user[2])
    return None

# Função para gerar um ID aleatório
def generate_random_id(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

######## ROTA DA PAGINA DE LOGIN E REGISTO 
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'register' in request.form:
            # Registo de utilizador
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['password2']

            if len(password) < 6:
                flash('The password must contain at least 6 characters.', category='danger')
            elif password != confirm_password:
                flash('Passwords do not match.', category='danger')
            else:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                try:
                    conexion = sqlite3.connect('book_trade.db')
                    cursor = conexion.cursor()
                    cursor.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', 
                    (name, email, hashed_password.decode('utf-8')))
                    conexion.commit()
                    conexion.close()
                    flash('Account created successfully! You can now log in.', category='success')
                except sqlite3.IntegrityError:
                    flash('This email is already registered.', category='danger')
                return redirect(url_for('login'))

        elif 'login' in request.form:
            # Login de utilizador
            email = request.form['signinEmail']
            password = request.form['signinPassword']

            conexion = sqlite3.connect('book_trade.db')
            cursor = conexion.cursor()
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            user = cursor.fetchone()
            conexion.close()

            if user:
                stored_password = user[3].encode('utf-8')  
                if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                    login_user(User(id=user[0], name=user[1], email=user[2]))
                    flash(f'Welcome, {user[1]}!', category='success')
                    return redirect(url_for('home'))
                else:
                    flash('Something went wrong. Please try again', category='danger')
            else:
                flash('Something went wrong. Please try again', category='danger')

    return render_template('login.html')

######## ROTA DA PAGINA PRINCIPAL HOME
@app.route('/home', methods=['GET'])
@login_required
def home():
    query = request.args.get('q', '')  # Obtém o valor da pesquisa (parâmetro 'q')

    conn = sqlite3.connect('book_trade.db')
    cursor = conn.cursor()

    try:
        # Consulta para filtrar os livros pelo título
        cursor.execute("""
            SELECT b.id, b.title, b.author, b.genre, b.image_url, b.dateAdded, u.name AS user_name
            FROM books b
            INNER JOIN users u ON b.user_id = u.id
            WHERE b.title LIKE :query
        """, {'query': '%' + query + '%'})

        books = cursor.fetchall()

        # Buscar os IDs dos livros na wishlist e tradelist do usuário atual
        cursor.execute('SELECT book_id FROM wishlist WHERE user_id = ?', (current_user.id,))
        wishlist_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute('SELECT book_id FROM tradelist WHERE user_id = ?', (current_user.id,))
        tradelist_ids = [row[0] for row in cursor.fetchall()]

    except Exception as e:
        flash(f'An error occurred while fetching books: {str(e)}', category='danger')
        books = []
        wishlist_ids = []
        tradelist_ids = []
    finally:
        conn.close()  

    return render_template('index.html', books=books, query=query, wishlist_ids=wishlist_ids, tradelist_ids=tradelist_ids)

######## ROTA DA PAGINA RECOMMEND QUE TÊM OS LIVROS TODOS COM OPÇÃO DE ADICIONAR A WISHLIST E PEDIR TROCA 
@app.route('/recommend', methods=['GET', 'POST'])
@login_required
def recommend():
    if request.method == 'POST':
        book_id = request.form.get('book_id')
        user_id = current_user.id

        # Conectar ao banco de dados
        try:
            conexion = sqlite3.connect('book_trade.db')
            cursor = conexion.cursor()

            # Verificar se o livro já está na wishlist do usuário
            cursor.execute('SELECT * FROM wishlist WHERE book_id = ? AND user_id = ?', (book_id, user_id))
            existing_entry = cursor.fetchone()

            if existing_entry:
                flash('This book is already in your wishlist!', category='danger')
            else:
                wishlist_id = generate_random_id(length=10)
                cursor.execute('INSERT INTO wishlist (id, book_id, user_id, status) VALUES (?, ?, ?, ?)',
                               (wishlist_id, book_id, user_id, 'Active'))
                conexion.commit()
                flash('Book added to wishlist successfully!', category='success')

        except Exception as e:
            flash(f'An error occurred: {str(e)}', category='danger')
        finally:
            conexion.close()

    try:
        # Recuperar os livros com dados do usuário
        conexion = sqlite3.connect('book_trade.db')
        cursor = conexion.cursor()

        # Buscar todos os livros
        cursor.execute('''
            SELECT books.id, books.author, books.title, books.genre, books.dateAdded, books.image_url, users.name
            FROM books
            INNER JOIN users ON books.user_id = users.id
            ORDER BY books.dateAdded DESC
        ''')
        books = cursor.fetchall()

        # Buscar os IDs dos livros na wishlist e tradelist do usuário atual
        cursor.execute('SELECT book_id FROM wishlist WHERE user_id = ?', (current_user.id,))
        wishlist_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute('SELECT book_id FROM tradelist WHERE user_id = ?', (current_user.id,))
        tradelist_ids = [row[0] for row in cursor.fetchall()]

    except Exception as e:
        flash(f'An error occurred while fetching books: {str(e)}', category='danger')
        books = []
        wishlist_ids = []
        tradelist_ids = []
    finally:
        conexion.close()

    # Passar os livros, wishlist e tradelist para o template
    return render_template("recommend.html", books=books, wishlist_ids=wishlist_ids, tradelist_ids=tradelist_ids)

####### ROTA EXTRA PARA OS LIVROS SEREM ADICIONADOS A TRADELIST (tabela da base de dados) pagina trade.html 
@app.route('/request-change', methods=['POST'])
@login_required
def request_change():
    # Obter o ID do livro a partir do formulário
    book_id = request.form.get('book_id')
    user_id = current_user.id

    # Conectar ao banco de dados
    conexion = sqlite3.connect('book_trade.db')
    cursor = conexion.cursor()

    try:
        # Verificar se o livro está na tradelist
        cursor.execute('SELECT * FROM tradelist WHERE book_id = ? AND user_id = ?', (book_id, user_id))
        tradelist_entry = cursor.fetchone()

        if tradelist_entry:
            # Se o livro já estiver na tradelist, removê-lo
            cursor.execute('DELETE FROM tradelist WHERE book_id = ? AND user_id = ?', (book_id, user_id))
            conexion.commit()

            flash('Book removed from tradelist.', category='success')
        else:
            # Se o livro não estiver na tradelist, adicionar à tradelist
            tradelist_id = generate_random_id(length=10)
            cursor.execute('INSERT INTO tradelist (id, book_id, user_id, status) VALUES (?, ?, ?, ?)',
                           (tradelist_id, book_id, user_id, 'Active'))
            conexion.commit()

            flash('Book successfully added to tradelist!', category='success')

    except Exception as e:
        flash(f'An error occurred: {str(e)}', category='danger')

    finally:
        conexion.close()

    # Redirecionar de volta para a página atual ou página de recomendação
    return redirect(url_for('trade'))

###### ROTA DA PAGINA DE TROCA DE LIVROS ONDE MOSTRA OS LIVROS QUE ESTÃO NA TRADELIST DE CADA UTILIZADOR 
@app.route('/trade')
@login_required
def trade():
    # Conectar ao banco de dados
    conexion = sqlite3.connect('book_trade.db')
    cursor = conexion.cursor()

    # Consulta para obter livros que estão na tradelist do usuário logado
    cursor.execute(''' 
        SELECT books.id, books.title, books.author, books.genre, books.image_url, books.dateAdded, users.name AS user_name
        FROM books
        INNER JOIN tradelist ON books.id = tradelist.book_id
        INNER JOIN users ON books.user_id = users.id
        WHERE tradelist.user_id = ? AND status = 'Active'
    ''', (current_user.id,))

    books = cursor.fetchall()
    conexion.close()

    return render_template('trade.html', books=books)

# Atualiza o status do livro para "Offered" ao propor uma troca
@app.route('/make-offer', methods=['POST'])
@login_required
def create_offer():
    # Obtém os dados enviados do formulário
    tradelist_book_id = request.form.get('book_id')  # Livro oferecido pelo usuário logado
    target_book_id = request.form.get('target_book_id')  # Livro pretendido pelo usuário logado

    # Verifique se ambos os parâmetros foram fornecidos
    if not tradelist_book_id or not target_book_id:
        return "Missing tradelistBookId or targetBookId", 400

    # Conectar ao banco de dados
    conexion = sqlite3.connect('book_trade.db')
    cursor = conexion.cursor()

    try:
        # Verificar se o livro da tradelist pertence ao usuário logado
        cursor.execute('''SELECT book_id FROM tradelist WHERE book_id = ? AND user_id = ?''', 
                       (tradelist_book_id, current_user.id))
        tradelist_entry = cursor.fetchone()

        if not tradelist_entry:
            flash("The book is not in your tradelist", "danger")
            return redirect(url_for('trade'))

        # Obter os detalhes do livro oferecido na tabela books
        cursor.execute('''SELECT id, user_id FROM books WHERE id = ?''', (tradelist_book_id,))
        offered_book = cursor.fetchone()

        if not offered_book:
            return "The offered book was not found in the books table", 404

        # Obter as variáveis necessárias para a tabela offer
        bookA_id = tradelist_book_id  # Livro oferecido
        userA_id = offered_book[1]    # user_id do livro oferecido
        bookB_id = target_book_id     # Livro pretendido
        userB_id = current_user.id    # user_id do livro pretendido

        # Verificar se o usuário está tentando trocar com ele mesmo
        if userA_id == userB_id:
            flash("You cannot offer books from your own collection to yourself!", "danger")
            return redirect(url_for('trade'))  # Redireciona para a página de ofertas com erro

        # Verificar se já existe uma oferta pendente entre os dois livros (em qualquer direção)
        cursor.execute('''
            SELECT * FROM offer 
            WHERE (bookA_id = ? AND bookB_id = ? AND status = "Pending") 
               OR (bookA_id = ? AND bookB_id = ? AND status = "Pending")
        ''', (bookA_id, bookB_id, bookB_id, bookA_id))

        existing_offer = cursor.fetchone()

        if existing_offer:
            flash("An offer already exists between these two books. Check your offers.", "danger")
            return redirect(url_for('trade'))  # Redireciona para a página de ofertas com erro

        # Criar o ID para a oferta
        offer_id = generate_random_id(length=10)

        # Inserir os dados na tabela offer
        cursor.execute(''' 
            INSERT INTO offer (id, bookA_id, userA_id, bookB_id, userB_id, status)
            VALUES (?, ?, ?, ?, ?, "Pending")
        ''', (offer_id, bookA_id, userA_id, bookB_id, userB_id))

        conexion.commit()
        # Mensagem de sucesso
        flash('Offer created successfully!', 'success')

        # Redirecionar para a página 'trade'
        return redirect(url_for('trade'))  # Ajuste o nome da função 'trade' para o nome correto da sua rota

    except Exception as e:
        conexion.rollback()
        return f"Error creating offer: {str(e)}", 500

    finally:
        conexion.close()

#Função para ver todos os livros quando o utilizador carrega no botão "Make an Offer no "Trade""
@app.route('/get-all-books')
@login_required
def get_all_books():
    try:
        # Pass the current user's ID to the function
        user_id = current_user.id
        books = get_all_books_from_db(user_id)  # Pass the user_id here
        books_data = [
            {
                'id': book['id'],
                'title': book['title'],
                'author': book['author'],
                'image_url': book['image_url'],
                'user_id': book['user_id'],
            }
            for book in books
        ]
        return jsonify(books_data)
    except Exception as e:
        return jsonify({"error": "Failed to fetch books"}), 500

def get_all_books_from_db(user_id):
    # Conectar ao banco de dados SQLite (ou ao seu banco de dados apropriado)
    conn = sqlite3.connect('book_trade.db')  # Substitua pelo caminho real do seu banco de dados
    cursor = conn.cursor()

    # Consulta para pegar todos os livros
    query = "SELECT id, title, author, image_url, user_id FROM books"
    
    # Execute a consulta no banco de dados e obtenha os resultados
    cursor.execute(query)
    books = cursor.fetchall()

    # Fechar a conexão com o banco de dados
    conn.close()

    # Filtrando os livros para retornar apenas os do usuário logado
    filtered_books = [book for book in books if book[4] == user_id]

    # Convertendo o resultado filtrado para uma lista de dicionários
    return [{
        "id": book[0],  # id do livro
        "title": book[1],  # título do livro
        "author": book[2],  # autor do livro
        "image_url": book[3],  # URL da imagem do livro
        "user_id": book[4]  # ID do usuário ao qual o livro pertence
    } for book in filtered_books]

####### ROTA DA PAGINA WISHLIST ONDE MOSTRA TODOS OS LIVROS QUE O UTILIZADOR ADICIONOU A WISHLIST (tabela da base de dados)
@app.route('/wishlist', methods=['GET', 'POST'])
@login_required
def wishlist():
    # Verificar se o utilizador removeu um livro da wishlist
    if request.method == 'POST':
        book_id = request.form.get('book_id')
        user_id = current_user.id

        try:
            # Conectando ao banco de dados
            conexion = sqlite3.connect('book_trade.db')
            cursor = conexion.cursor()

            # Remover o livro da wishlist do usuário
            cursor.execute('DELETE FROM wishlist WHERE book_id = ? AND user_id = ?', (book_id, user_id))
            conexion.commit()
            flash('Book removed from wishlist successfully!', category='success')
        except Exception as e:
            flash(f'An error occurred: {str(e)}', category='danger')
        finally:
            conexion.close()

    # Recuperar os livros com dados do usuário da wishlist
    conexion = sqlite3.connect('book_trade.db')
    cursor = conexion.cursor()
    cursor.execute(''' 
        SELECT b.id, b.author, b.title, b.genre, b.dateAdded, b.image_url
        FROM wishlist w
        JOIN books b ON w.book_id = b.id
        WHERE w.status = 'Active' AND w.user_id = ?
    ''', (current_user.id,))
    books = cursor.fetchall()

    # Consultar os IDs dos livros da tradelist do usuário
    cursor.execute('SELECT book_id FROM tradelist WHERE user_id = ?', (current_user.id,))
    tradelist_ids = [row[0] for row in cursor.fetchall()]

    conexion.close()

    # Passando os livros da wishlist e os IDs da tradelist para o template
    return render_template('wishlist.html', books=books, tradelist_ids=tradelist_ids)

###### ROTA EXTRA PARA ADICIONAR LIVROS A APLICAÇÃO. É FEITO NA PAGINA home.html
@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def user():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        genre = request.form.get('genre')
        image_url = request.form.get('image_url')  

        # Verificando se a URL fornecida é válida
        if not image_url:
            flash('Book cover URL is required.', category='danger')
            return redirect(url_for('user'))

        # Validando o link da imagem
        if not image_url.startswith(('http://', 'https://')):
            flash('Please provide a valid URL for the book cover.', category='danger')
            return redirect(url_for('user'))

        # Gerando um ID aleatório para o livro
        book_id = generate_random_id()

        # Formatando a data para o formato dia-mês-ano
        formatted_date = date.today().strftime('%d-%m-%Y')

        try:
            # Inserindo os dados na tabela 'books'
            conexion = sqlite3.connect('book_trade.db')
            cursor = conexion.cursor()
            cursor.execute('INSERT INTO books (id, title, author, genre, image_url, user_id, dateAdded) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                        (book_id, title, author, genre, image_url, current_user.id, formatted_date))
            conexion.commit()
            conexion.close()
            flash('Book added successfully!', category='success')
        except Exception as e:
            flash(f'An error occurred: {str(e)}', category='danger')

    return render_template('add_book.html')

######## ROTA EXTRA PARA O UTILIZADOR CONFIGURAR ALGUMAS INFORMAÇÕES PESSOAIS. É feito na página home.html
@app.route('/user', methods=['GET', 'POST'])
@login_required
def user_view():
    # Obtendo o ID do usuário logado
    user_id = current_user.id  # Flask-Login cuida disso

    # Conectar ao banco de dados para obter os dados do usuário
    conn = sqlite3.connect('book_trade.db')
    conn.row_factory = sqlite3.Row  # Para obter as colunas como dicionários
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()

    if not user:
        conn.close()
        flash('User not found.', 'danger')
        return redirect(url_for('home'))

    # Consultar livros adicionados pelo usuário
    books = conn.execute('SELECT * FROM books WHERE user_id = ?', (user_id,)).fetchall()
    conn.close()

    if request.method == 'POST':
        if 'remove_book' in request.form:  # Verifica se é uma ação de remoção
            book_id = request.form.get('book_id')

            if not book_id:
                flash('Book ID is required to remove a book.', 'danger')
                return redirect(url_for('user_view'))

            # Verificar se o livro pertence ao usuário atual antes de remover
            conn = sqlite3.connect('book_trade.db')
            try:
                result = conn.execute(
                    'DELETE FROM books WHERE id = ? AND user_id = ?',
                    (book_id, user_id)
                )
                conn.commit()

                if result.rowcount > 0:
                    flash('Book removed successfully!', 'success')
                else:
                    flash('Book not found or does not belong to you.', 'danger')

            except sqlite3.Error as e:
                flash('An error occurred while removing the book.', 'danger')
                print(f"Database error: {e}")  # Log para debug

            finally:
                conn.close()

            return redirect(url_for('user_view'))

        else:  # Atualização de informações do usuário
            name = request.form.get('name', '').strip()  # Remover espaços em branco extras
            phone = request.form.get('phone', '').strip()

            # Verificação de dados obrigatórios
            if not name:
                flash('Name is mandatory!', 'danger')
                return redirect(url_for('user_view'))

            # Validação do número de telefone
            if phone and not phone.isdigit():
                flash('Phone number must contain only digits.', 'danger')
                return redirect(url_for('user_view'))
            if phone and len(phone) != 9:
                flash('Phone number must be exactly 9 digits.', 'danger')
                return redirect(url_for('user_view'))
            phone = phone if phone else None  # Salvar como NULL se o campo estiver vazio

            # Verificar se houve alteração nos dados
            if name == user['name'] and phone == user['phone']:
                flash('No changes detected. The same data cannot be saved.', 'danger')
                return redirect(url_for('user_view'))

            # Atualizar os dados na base de dados
            conn = sqlite3.connect('book_trade.db')
            try:
                conn.execute(''' 
                    UPDATE users 
                    SET name = ?, phone = ? 
                    WHERE id = ? 
                ''', (name, phone, user_id))

                conn.commit()
                flash('Your information was updated successfully!', 'success')

            except sqlite3.Error as e:
                flash('An error occurred while updating your information.', 'danger')
                print(f"Database error: {e}")  # Log para debug

            finally:
                conn.close()

            return redirect(url_for('user_view'))

    # Garantir que o valor de phone seja tratado como string vazia se for NULL
    user_dict = dict(user)
    user_dict['phone'] = user_dict['phone'] if user_dict['phone'] else ''

    # Transformar livros em lista de dicionários
    books_list = [dict(book) for book in books]

    return render_template('user.html', user=user_dict, books=books_list)

@app.route('/offer', methods=['GET', 'POST'])
@login_required
def offer():
    # Conectar ao banco de dados
    conexion = sqlite3.connect('book_trade.db')
    cursor = conexion.cursor()

    if request.method == 'POST':
        offer_id = request.form.get('offer_id')
        action = request.form.get('action')  # Pode ser 'accept', 'deny' ou 'cancel'

        try:
            if action == 'accept':
                # Aceitar a oferta e realizar a troca
                cursor.execute('''
                    SELECT bookA_id, bookB_id FROM offer WHERE id = ?
                ''', (offer_id,))
                books = cursor.fetchone()

                if books:
                    bookA_id, bookB_id = books
                    cursor.execute('''
                        DELETE FROM offer WHERE id = ?
                    ''', (offer_id,))
                    cursor.execute('''
                        DELETE FROM books WHERE id = ? OR id = ?
                    ''', (bookA_id, bookB_id))
                    flash("Offer accepted and books exchanged.", "success")
                else:
                    flash("Offer not found.", "danger")

            elif action == 'deny':
                # Negar a oferta
                cursor.execute('''
                    DELETE FROM offer WHERE id = ?
                ''', (offer_id,))
                flash("Offer denied.", "success")

            elif action == 'cancel':
                # Cancelar a troca
                cursor.execute('''
                    DELETE FROM offer WHERE id = ?
                ''', (offer_id,))
                flash("Trade canceled successfully.", "success")

            # Commit das alterações no banco de dados
            conexion.commit()

        except Exception as e:
            flash(f"Error processing the offer: {str(e)}", "danger")
            conexion.rollback()

        return redirect(url_for('offer'))

    try:
        # Obter as ofertas enviadas
        cursor.execute('''
            SELECT o.id, b1.title AS offered_book, b2.title AS target_book, o.status, b1.image_url AS offered_book_image, b2.image_url AS target_book_image
            FROM offer o
            JOIN books b1 ON o.bookA_id = b1.id
            JOIN books b2 ON o.bookB_id = b2.id
            WHERE o.userB_id = ?
        ''', (current_user.id,))
        sent_offers = cursor.fetchall()

        # Obter as ofertas recebidas
        cursor.execute('''
            SELECT o.id, b1.title AS offered_book, b2.title AS target_book, o.status, b1.image_url AS offered_book_image, b2.image_url AS target_book_image
            FROM offer o
            JOIN books b1 ON o.bookA_id = b1.id
            JOIN books b2 ON o.bookB_id = b2.id
            WHERE o.userA_id = ?
        ''', (current_user.id,))
        received_offers = cursor.fetchall()

        # Render Template
        return render_template('offer.html', sent_offers=sent_offers, received_offers=received_offers)

    except Exception as e:
        flash(f"Error retrieving offers: {str(e)}", "danger")
        return redirect(url_for('trade'))

    finally:
        conexion.close()

##### ROTA EXTRA PARA O UTILIZADOR FAZER LOGOUT DA APLICAÇÃO. É feito na pagina home.html 
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', category='info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()  
    app.run(debug=True)