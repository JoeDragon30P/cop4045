"""
Problem 5: Web Comment board Application (Flask + Jinja2 + session + CSV Persistence)
"""

from flask import Flask, render_template, request, session, redirect, url_for
import csv
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'cop4045_joseph_majcherek_secret_key'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COMMENTS_FILE = os.path.join(BASE_DIR, 'comments.csv')

def init_csv():
    """Initialize the CSV file with headers if it doesn't exist."""
    if not os.path.exists(COMMENTS_FILE):
        with open(COMMENTS_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Username', 'Hashtags', 'Comment', 'Timestamp'])

def get_all_comments():
    """Read all comments from the CSV file."""
    init_csv()
    comments = []
    try:
        with open(COMMENTS_FILE, 'r', newline='') as f:
            reader = csv.DictReader(f)
            if reader.fieldnames:
                for row in reader:
                    comments.append(row)
    except (FileNotFoundError, ValueError):
        pass
    return comments

def save_comment(username, hashtags, comment_text):
    """Save a comment to the CSV file."""
    init_csv()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(COMMENTS_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([username, hashtags, comment_text, timestamp])

def search_comments(search_text='', author=''):
    """Search comments by text/hashtags and author."""
    comments = get_all_comments()
    filtered = []
    
    search_text = search_text.strip().lower()
    author = author.strip().lower()
    
    for comment in comments:
        # Filter by author if provided
        if author and comment['Username'].lower() != author:
            continue
        
        # Filter by search text if provided (search in hashtags and comment)
        if search_text:
            comment_lower = comment['Comment'].lower()
            hashtags_lower = comment['Hashtags'].lower()
            if search_text not in comment_lower and search_text not in hashtags_lower:
                continue
        
        filtered.append(comment)
    
    return filtered

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        hashtags = request.form.get('hashtags', '').strip()
        comment_text = request.form.get('comment', '').strip()
        
        if username and comment_text:
            session['username'] = username
            save_comment(username, hashtags, comment_text)
            return redirect(url_for('index'))
    
    username = session.get('username', '')
    comments = get_all_comments()
    
    return render_template('index.html', username=username, comments=comments)

@app.route('/search', methods=['GET'])
def search():
    search_text = request.args.get('search_text', '').strip()
    author = request.args.get('author', '').strip()
    
    results = search_comments(search_text=search_text, author=author)
    
    return render_template(
        'search.html', 
        search_text=search_text, 
        author=author, 
        results=results, 
        result_count=len(results)
    )

if __name__ == '__main__':
    app.run(debug=True)
