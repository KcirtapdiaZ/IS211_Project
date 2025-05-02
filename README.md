# IS211_Project
I chose option 2, which is the blog application.

This is a simple Flask-based blog application that allows users to log in, create, edit, view, and delete blog posts. It uses SQLite for the database and implements basic functionality for user authentication and managing blog content.

The Flask Blog App lets users log in, create, view, edit, and delete blog posts. It uses Flask for the web framework and SQLAlchemy to interact with a SQLite database. The app has two main parts: a Post model for storing blog posts and a User model for managing logins. When a user logs in, their credentials are checked against the database. Once logged in, users can manage posts through a dashboard. The app uses sessions to keep track of who’s logged in and ensures that only logged-in users can create, edit, or delete posts. The database is automatically set up when the app starts.

Features

User login
Create, edit, and delete posts
View posts on the homepage
Session management for logged-in users

Setup

Requirements
Python 3.x
Flask
Flask-SQLAlchemy

Routes
/: View all posts.
/login: Log in with a username and password.
/dashboard: Manage your posts (requires login).
/new_post: Create a new post (requires login).
/edit_post/<post_id>: Edit a post (requires login).
/delete_post/<post_id>: Delete a post (requires login).
/logout: Log out.
