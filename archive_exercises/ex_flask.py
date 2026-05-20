# 1. מייבאים גם את url_for
from flask import Flask, url_for 

app = Flask(__name__)

# דף הבית הראשי
@app.route('/')
def home():
    # 2. אנחנו מבקשים מ-url_for לייצר קישור לפונקציה show_article
    # ומעבירים לה את ה-slug שאנחנו רוצים
    link_hello = url_for('show_article', slug='hello')
    link_python = url_for('show_article', slug='python-tips')
    
    # הקישורים שיוצרו מוכנסים ישירות לתוך קוד ה-HTML
    return f'''
        <h1>ברוכים הבאים לבלוג שלי!</h1>
        <p>בחר מאמר לקריאה:</p>
        <ul>
            <li><a href="{link_hello}">מאמר ראשון (hello)</a></li>
            <li><a href="{link_python}">טיפים לפייתון (python-tips)</a></li>
        </ul>
    '''

# דף המאמר הדינמי
@app.route('/article/<slug>')
def show_article(slug):
    return f"<h1>תוכן המאמר: {slug}</h1><p><a href='/'>חזרה לדף הבית</a></p>"

if __name__ == '__main__':
    app.run(debug=True)
