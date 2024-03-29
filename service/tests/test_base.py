import tempfile
import unittest as unittest
import warnings

from app import create_app
from extensions import db
from sqlalchemy.orm.session import close_all_sessions

warnings.filterwarnings("ignore")


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        app = create_app(testing=True)
        self.test_db_file = tempfile.mkstemp()[1]

        with app.app_context():
            db.create_all()

        app.app_context().push()
        self.app = app.test_client()

    def tearDown(self):
        db.session.rollback()
        close_all_sessions()
        db.drop_all()
