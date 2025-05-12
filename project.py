from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Initialize Flask app and configure database
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

# Define the User model (for demonstration purposes, assuming a basic model for login)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Run this function before every request to ensure the tables are created
@app.before_request
def create_tables():
    db.create_all()

# Route to the homepage that shows the list of posts
@app.route('/')
def index():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('index.html', posts=posts)

# Route to login page (for demonstration purposes)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Assuming a simple check for demo purposes (not secure for production)
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials, please try again.', 'danger')
    return render_template('login.html')

# Route to dashboard page for logged-in users
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('You must be logged in to access the dashboard', 'danger')
        return redirect(url_for('login'))
    
    posts = Post.query.all()
    return render_template('dashboard.html', posts=posts)

# Route to create a new post
@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if 'user_id' not in session:
        flash('You must be logged in to create a post', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('new_post.html')

# Route to edit a post
@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if 'user_id' not in session:
        flash('You must be logged in to edit a post', 'danger')
        return redirect(url_for('login'))
    
    post = Post.query.get_or_404(post_id)
    
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('edit_post.html', post=post)

# Route to delete a post
@app.route('/delete_post/<int:post_id>', methods=['GET', 'POST'])
def delete_post(post_id):
    if 'user_id' not in session:
        flash('You must be logged in to delete a post', 'danger')
        return redirect(url_for('login'))
    
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

# Route to log out
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))

# Run the app
# Add this function to create a sample user
def create_sample_user():
    user = User.query.filter_by(username='admin').first()
    if not user:
        sample_user = User(username='admin', password='password123')
        db.session.add(sample_user)
        db.session.commit()
        print("Sample user created: Username: admin, Password: password123")

if __name__ == '__main__':
    with app.app_context():
        create_sample_user()  # Ensure sample user is created on app start
    app.run(debug=True)


