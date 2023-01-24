from app import app
from models import db, Users, Post
from unittest import TestCase

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blogly_test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()

class BloglyTestCase(TestCase):

    def setUp(self):
        '''Clean up any existing User and Post before the next text is run'''
        Users.query.delete()
        Post.query.delete()
        user = Users(first_name='John', last_name='Wick')
        post = Post(title='How to become a Jujitsu master',
                    content='You need to spend many years training',
                    user_id=1)
        db.session.add(user)
        db.session.commit()
        db.session.add(post)
        db.session.commit()

    def tearDown(self):
        '''Clean up any fouled transaction in a db.session'''
        db.session.rollback()

    def test_home(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('How to become a Jujitsu master', html)

    def test_show_all_users(self):
        with app.test_client() as client:
            res = client.get('/users')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Wick, John', html)

    # def test_create_new_user(self):
    #     with app.test_client() as client:
    #         d = {"first-name":"Luke", "last-name":"Skywalker"}
    #         res = client.post('/users/new', data=d, follow_redirects=True)
    #         html = res.get_data(as_text=True)

    #         self.assertEqual(res.status_code, 200)
    #         self.assertIn('Skywalker, Luke', html)

    def test_show_user_page(self):
        with app.test_client() as client:
            res = client.get(f'/users/{1}')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('John Wick', html)

    def test_update_user(self):
        with app.test_client() as client:
            d = {"first-name":"Luke", "last-name":"Skywalker"}
            res = client.post(f'/users/{1}/edit', data=d, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Skywalker, Luke', html)
    
   