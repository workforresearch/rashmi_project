import sys
import sqlite3
import logging
from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

# build format
format_output = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# build StreamHandler for sys.stderr                                                                                                   
error = logging.StreamHandler(stream=sys.stderr)
error.setLevel(logging.DEBUG)
error.setFormatter(format_output)

# build StreamHandler for sys.stdout
out = logging.StreamHandler(stream=sys.stdout)
out.setFormatter(format_output)
out.setLevel(logging.DEBUG)

root = logging.getLogger()
root.addHandler(out)
root.addHandler(error)



connection_number=0
post_count = 0

def get_db_connection():
    global connection_number
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    connection_number +=1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection_number = len(posts)
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        return render_template('404.html'), 404
    else:
        return render_template('post.html', post=post)



# Define the About Us page
@app.route('/about')
def about():
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            return redirect(url_for('index'))
    return render_template('create.html')



# define the endpoints for health check status
@app.route('/healthz')
def status():
    response = app.response_class(
        response=json.dumps({"result":"OK - healthy"}),
        status=200,
        mimetype='application/json'
  ) 
    return response    


# define the matrics endpoints
@app.route('/metrics')
def metrics():
    global connection_number
    post_count = get_post_count()
    response = app.response_class(
        response=json.dumps({"status":"success","code":0,"data":{"db_connection_count": connection_number, "post_count": post_count}}),
        status=200,
        mimetype='application/json'
  )
    return response


def get_post_count():
    connection = get_db_connection()
    
    posts = connection.execute('SELECT * FROM posts').fetchall()
                     
    connection.close()
    return len(posts)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='3111')
