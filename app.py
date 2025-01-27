from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user

app = Flask(__name__, template_folder='views')
app.secret_key = 'your_secret_key'  # Ganti dengan kunci rahasia untuk sesi pengguna

# Konfigurasi Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Koneksi Database
def get_db():
    try:
        connection = mysql.connector.connect(
            host="2rco1.h.filess.io",
            database="perpustakaan_antsguide",
            user="perpustakaan_antsguide",
            password="c063d26ee1e95adb77118e516649be46123d1521",
            port="3306"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

def execute_query(query, params=None):
    connection = get_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        connection.commit()
        cursor.close()
        connection.close()

def fetch_one(query, params=None):
    connection = get_db()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        record = cursor.fetchone()
        cursor.close()
        connection.close()
        return record

def fetch_all(query, params=None):
    connection = get_db()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        return records

# Model User untuk Flask-Login
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

    def get_id(self):
        return str(self.id)

# Loader untuk mengembalikan user berdasarkan ID
@login_manager.user_loader
def load_user(user_id):
    user = fetch_one("SELECT * FROM users WHERE id = %s", (user_id,))
    if user:
        return User(user['id'], user['username'])
    return None

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        email = request.form['email']

        # Cek jika username atau email sudah terdaftar
        existing_user = fetch_one("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
        if existing_user:
            flash('Username atau email sudah terdaftar!', 'danger')
            return redirect(url_for('register'))
        
        try:
            execute_query("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
            flash('Registrasi berhasil! Silakan login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error: {e}', 'danger')
            return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = fetch_one("SELECT * FROM users WHERE username = %s", (username,))
        if user and check_password_hash(user['password'], password):
            user_obj = User(user['id'], user['username'])
            login_user(user_obj)
            flash('Login berhasil!', 'success')
            return redirect(url_for('dashboard'))
        flash('Username atau password salah!', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    borrowings = fetch_all(""" 
        SELECT b.title, br.borrow_date, br.return_date, br.status
        FROM borrowings br
        JOIN books b ON br.book_id = b.id
        WHERE br.user_id = %s
    """, (current_user.id,))
    return render_template('dashboard.html', borrowings=borrowings)

@app.route('/books')
@login_required
def books():
    available_books = fetch_all("SELECT * FROM books WHERE copies_available > 0")
    return render_template('books.html', books=available_books)

@app.route('/borrow/<int:book_id>', methods=['POST'])
@login_required
def borrow_book(book_id):
    book = fetch_one("SELECT * FROM books WHERE id = %s", (book_id,))
    if book and book['copies_available'] > 0:
        execute_query("INSERT INTO borrowings (user_id, book_id, borrow_date) VALUES (%s, %s, NOW())", (current_user.id, book_id))
        execute_query("UPDATE books SET copies_available = copies_available - 1 WHERE id = %s", (book_id,))
        flash('Buku berhasil dipinjam!', 'success')
    else:
        flash('Buku tidak tersedia!', 'danger')
    return redirect(url_for('books'))

@app.route('/return/<int:book_id>', methods=['POST'])
@login_required
def return_book(book_id):
    borrowing = fetch_one("SELECT * FROM borrowings WHERE user_id = %s AND book_id = %s AND status = 'borrowed'", (current_user.id, book_id))
    if borrowing:
        execute_query("UPDATE borrowings SET return_date = NOW(), status = 'returned' WHERE id = %s", (borrowing['id'],))
        execute_query("UPDATE books SET copies_available = copies_available + 1 WHERE id = %s", (book_id,))
        flash('Buku berhasil dikembalikan!', 'success')
    else:
        flash('Buku belum dipinjam atau sudah dikembalikan.', 'danger')
    return redirect(url_for('dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Anda telah logout.', 'success')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
