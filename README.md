# Blogly Blog

## Blogly is a work in progress. This is only part one of the blogly project.

## Working Features
**Home page**
- viewing 10 most recent posts sorted by date of creation
**Users management**
- view all users (through Sign Up link)
- add new users
**User page**
- edit existing user
- delete existing user
- add new posts
- view user posts
**Post CRUD**
- creating new post with title, content and tags
- view post with tags included
- edit post
- delete post

**Features that are not working (coming soon)**
- Loging/Sign up

### How to get started with Blogly blog
1. Download the zip file and extract the contents.
2. Using terminal go to the location of the file and open it
3. Create a virtual environment 
  - `python -m venv venv`
4. Activate the virtual environment to containarize installation of required python packages
  - `venv\scripts\activate`
  - you'll know that venv has been activated when you see (venv) infront of your directory path
5. Install required python packages for the poject that are listed in requirements.txt file
  - `pip install -r requirements.txt`
6. Run Blogly blog in the terminal window
  - `python app.py`

### Database 

The test database is included with this app. You'll find blogly.db file in an instance directory, and it will work right out of the box. 

**How to create database file if it was not provided?**
- Inside of the **app.py** file we set app.config to indicate which database we'll be using and what name it should have. 
- In this case we are using SQLite because it comes built with python and therefore no additional packages or files need to be installed. 

`app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blogly.db"`

- Next we need to connect  our application to SQLAlchemy, which we handle in the **models.py** and import those functions into **app.py**.

`from models import db, connect_db, Users`

- We use connect_db() function to connect app to SQLAlchemy.

`connect_db(app)`

*Another way of connecting application to SQLAlchemy is if we wanted to keep all our code in one file.* Inside **app.py**:

`db = SQLAlchemy(app)`

- Next we use a function to allow terminal to interact with out app. We'll need to use the terminal to actually create the datatable Users from the **models.py** file.

 `app.app_context().push()`
 
 We are done with set up, but the database and the datatables have not been created yet. 
 
 #### Creating a Data table 'users'
 
 In the terminal while the (venv) virtual environment is activated, you'll need to enter an interactive python shell by typing **python**
 - Once inside the python interactive shell:
 ```
 from app import db
 db.create_all()
 ```
 create_all() function create the tables based on the 'users' schemas provided in the **models.py** file. This only needs to be run once. You can exit python interactive shell by pressing *Ctrl+Z* or typing *quit()*.
 
 - You'll see a new folder directory will be created 'instance' which will contain 'blogly.db' file. 
 - You can now run Blogly app
 - `python app.py`
 
