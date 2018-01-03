import logging
import os
import tempfile
import unittest

from pyui import pyui, model

LOG = logging.getLogger(__name__)


class PGPoolStatsTest(unittest.TestCase):
    def setUp(self):
        LOG.info("Configure Flask for testing")
        self.db_fd, self.db_path = tempfile.mkstemp()
        database_url = 'sqlite:///' + self.db_path
        model.init_db(database_url)
        model.create_tables()
        pyui.APP.testing = True
        self.app = pyui.APP.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.remove(self.db_path)

    def test_empty_database(self):
        response = self.app.get('/accounts')
        self.assertIn(b'No accounts', response.data)
