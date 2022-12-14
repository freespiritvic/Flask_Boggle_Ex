from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class FlaskTests(TestCase):

    def homepage_test(self):
        """Test the homepage route"""

        res = self.client.get('/')
        decoded = res.data.decode()
        self.assertIn("Score: 0", decoded)
        self.assertIn("Times Played: 0", decoded)
        self.assertIn("Top Score: 0", decoded)
        self.assertIn("board",session)
        self.assertIsNone(session.get("topscore"))
        self.assertIsNone(session.get("numplays"))

    def valid_word_test(self):
       """Test if a word is valid"""
      
       with self.client as client:
           with client.session_transaction() as sess:
               sess['board'] = [["R", "O", "K", "R", "T"],
                                ["C", "C", "T", "T", "T"],
                                ["C", "A", "T", "T", "T"],
                                ["C", "A", "T", "T", "T"],
                                ["C", "A", "T", "T", "T"]]
       response = self.client.get('/word_check?word=cat')
       self.assertEqual(response.json['response'], 'ok')

    def not_on_board_test(self):
       """Test if word is not on board"""
      
       with self.client as client:
           with client.session_transaction() as sess:
               sess['board'] = [["R", "O", "K", "R", "T"],
                                ["C", "C", "T", "T", "T"],
                                ["C", "A", "T", "T", "T"],
                                ["C", "A", "T", "T", "T"],
                                ["C", "A", "T", "T", "T"]]
       response = self.client.get('/word_check?word=roast')
       self.assertEqual(response.json['response'], 'not-on-board')

    def not_word_test(self):
       """test if a non-english word is submitted"""
      
       with self.client as client:
           with client.session_transaction() as sess:
               sess['board'] = [["R", "O", "K", "R", "T"],
                                ["C", "C", "T", "T", "T"],
                                ["C", "A", "T", "T", "T"],
                                ["C", "A", "T", "T", "T"],
                                ["C", "A", "T", "T", "T"]]
       response = self.client.get('/word_check?word=stupider')
       self.assertEqual(response.json['response'], 'not-word')