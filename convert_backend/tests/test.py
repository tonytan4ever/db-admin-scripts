import os
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models
from convert_backend import convert_existing_to_different_vendor

engine = create_engine("sqlite:////test_from_db.db", echo=False, convert_unicode=True)
Session = sessionmaker(bind=engine)
session = Session()

class TestConvertBackend(unittest.TestCase):
    
    def setUp(self):
        models.Base.metadata.create_all(engine)
        cloud = models.Cloud(
                name='private_cloud',
                description='a private cloud')
        session.add(cloud)
        session.add(models.Machine(
            hostname='zeus',
            description='application server',
            cloud=cloud,
            operating_system='Arch 64'))
        session.add(models.Machine(
            hostname='apollo',
            description='database server',
            cloud=cloud,
            operating_system='Arch 64'))
        session.add(models.Machine(
            hostname='hermes',
            description='messaging server',
            cloud=cloud,
            operating_system='Ubuntu 13.10 64'))
        session.commit()
        
        self.to_db_string = "sqlite:////test_to_db.db"
    
    def test_convert_logic(self):
        convert_existing_to_different_vendor.pull_data(
          "sqlite:////test_from_db.db",
          "sqlite:////test_to_db.db",
          ['*']
        )
        print "Backend conversion completed..."
    
    def tearDown(self):
        if os.path.exists('test_from_db.db'):
            os.remove('test_from_db.db')
        if os.path.exists('test_to_db.db'):
            os.remove('test_to_db.db')
