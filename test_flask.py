from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///Blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """ Tests for views for Users. """

    def setUp(self):
        """ Add a sample user. """

        User.query.delete()

        user = User(first_name="testFirst", last_name="testLast",
                    profile_img="testURL")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """ Clean up any fouled transactions. """

        db.session.rollback()

    def test_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('testFirst testLast', html)

    def test_user_information(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>User details</h2>', html)
            self.assertIn('<li>testFirst testLast</li>', html)
            self.assertIn('<img src="testURL" alt="testFirst">', html)

    def test_generate_form(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            self.assertEqual(resp.status_code, 200)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "testFirst2", "last_name": "testLast2",
                 "profile_img": "testURL2"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('testFirst2 testLast2', html)
