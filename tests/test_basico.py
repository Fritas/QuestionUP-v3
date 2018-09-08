"""
    UnitTest basico do sistema flask
"""

import unittest
from flask import current_app
from app import create_app, db

class BasicoTestCase(unittest.TestCase):
    def montar(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def desmontar(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_existe(self):
        self.assertFalse(current_app is None)

    def test_app_testing(self):
        self.assertTrue(current_app.config['TESTING'])