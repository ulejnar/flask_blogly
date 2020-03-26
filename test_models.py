# from unittest import TestCase

# from app import app
# from models import db, User

# # Use test database and don't clutter tests with SQL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///Blogly_test'
# app.config['SQLALCHEMY_ECHO'] = False

# db.drop_all()
# db.create_all()


# class UserModelTestCase(TestCase):
#     """Tests for model for Pets."""

#     def setUp(self):
#         """Clean up any existing pets."""

#         User.query.delete()

#     def tearDown(self):
#         """Clean up any fouled transaction."""

#         db.session.rollback()

#     def test_first_name(self):
#         """ Make sure first name input by user correctly enters database """

#         user = User(first_name="testFirst", last_name="testLast", profile_img="testURL")
#         user.first_name