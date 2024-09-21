import unittest

import mongomock
from mongoengine import connect, disconnect

from agents.db.epic import Epic


class TestDeviceChat(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        disconnect()
        connect('mongoenginetest', host='mongodb://localhost', mongo_client_class=mongomock.MongoClient)

        self.new_epic = Epic(description="Epic description",
                           stories=None).save()

    def test_find_epic(self):

         result = Epic.objects()
         assert len(result) == 1