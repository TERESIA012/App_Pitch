import unittest
from app.models import Pitches
from app import db

class PitchTest(unittest.TestCase):
    def setUp(self):
        self.new_pitch=Pitches(pitch=" app pitch",author="tess",title="business",id=1)
    def test_instance(self):
        self.assertTrue(isinstance(self.new_pitch,Pitches))
    def test_init(self):
        self.assertEqual(self.new_pitch.pitch,"app-pitch")
        self.assertEqual(self.new_pitch.author,"tess")
        self.assertEqual(self.new_pitch.title,"business")
        self.assertEqual(self.new_pitch.id,1)