from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import pyrebase
from firebase_config import auth
import yfinance as yf

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# SQLite Database connection
def get_db_connection():
    conn = sqlite3.connect('news.db')
    conn.row_factory = sqlite3.Row
    return conn

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Basic validation
        if password != confirm_password:
            return "Passwords do not match"

        try:
            # Register user in Firebase
            auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('login'))
        except:
            return "Error occurred during registration"

    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            # Authenticate with Firebase
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = user['idToken']
            return redirect(url_for('index'))
        except:
            return "Invalid credentials"
    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# Home route - List all sections
@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))

    return redirect(url_for('section', rss_title='all', page=1))

# Section route - List articles from a section with pagination
@app.route('/section/<rss_title>')
def section(rss_title):
    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    conn.row_factory = sqlite3.Row

    page = int(request.args.get('page', 1))  # Default page 1 if not provided
    per_page = 10  # Number of articles per page
    offset = (page - 1) * per_page

    # SQL query to get all sources for dropdown
    rss_array = conn.execute('SELECT DISTINCT source FROM articles').fetchall()

    # SQL query for pagination and showing the newest news first
    if rss_title == 'all':
        articles = conn.execute('''
            SELECT * FROM articles 
            ORDER BY published_date DESC 
            LIMIT ? OFFSET ?''', (per_page, offset)).fetchall()
        total_articles = conn.execute('SELECT COUNT(*) FROM articles').fetchone()[0]
    else:
        articles = conn.execute('''
            SELECT * FROM articles 
            WHERE source = ? 
            ORDER BY published_date DESC 
            LIMIT ? OFFSET ?''', (rss_title, per_page, offset)).fetchall()
        total_articles = conn.execute('SELECT COUNT(*) FROM articles WHERE source = ?', (rss_title,)).fetchone()[0]

    conn.close()

    # Calculate total pages for pagination
    total_pages = (total_articles + per_page - 1) // per_page

    return render_template('section.html', 
                           entries=articles, 
                           rss_title=rss_title, 
                           rss_array=rss_array, 
                           page=page, 
                           total_pages=total_pages)

# Article route - Show detailed article view
@app.route('/article/<rss_title>/<int:entry_index>')
def article(rss_title, entry_index):
    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    conn.row_factory = sqlite3.Row

    # Fetch the specific article
    article = conn.execute('SELECT * FROM articles WHERE id = ?', (entry_index,)).fetchone()

    # Fetch all sources for the navigation bar
    rss_array = conn.execute('SELECT DISTINCT source FROM articles').fetchall()

    conn.close()

    return render_template('article.html', entry=article, rss_title=rss_title, rss_array=rss_array)

# Search route
@app.route('/search', methods=['GET'])
def search():
    if 'user' not in session:
        return redirect(url_for('login'))

    search_query = request.args.get('query', '').strip()

    if search_query:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row

        # Perform a case-insensitive search for the query in the title and summary
        query = f"%{search_query}%"
        search_results = conn.execute('''
            SELECT * FROM articles 
            WHERE title LIKE ? OR summary LIKE ? OR content LIKE ?
        ''', (query, query, query)).fetchall()

        # Fetch all sources for the navigation bar
        rss_array = conn.execute('SELECT DISTINCT source FROM articles').fetchall()

        conn.close()

        return render_template('search_results.html', entries=search_results, rss_array=rss_array, search_query=search_query)
    
    return redirect(url_for('index'))

# Stock data fetching function
def fetch_stock_data():
    stocks = ['TCS.NS', 'RELIANCE.NS', 'INFY.NS', 'HDFCBANK.NS', 'ICICIBANK.NS']

    stock_data = []
    for stock in stocks:
        ticker = yf.Ticker(stock)
        # Fetch last two days' data to calculate the change
        data = ticker.history(period="5d")  

        if not data.empty and len(data) > 1:
            price = data['Close'].iloc[-1]
            previous_close = data['Close'].iloc[-2]
            change = price - previous_close
        else:
            # Handle cases with no data or only one day of data
            price = "N/A"
            change = 0

        stock_data.append({
            'ticker': stock,
            'price': f'{price:.2f}' if isinstance(price, (int, float)) else price,
            'change': f'{change:.2f}' if isinstance(price, (int, float)) and price != "N/A" else "N/A"
        })

    return stock_data


# Route to get stock data
@app.route('/stocks')
def get_stocks():
    try:
        stock_data = fetch_stock_data()
        return jsonify(stock_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=5001) 
