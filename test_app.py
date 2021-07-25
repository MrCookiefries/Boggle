from unittest import TestCase
from app import app
from flask import session, jsonify
from boggle import Boggle

app.config["TESTING"] = True
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

class FlaskTests(TestCase):

    def setUp(self):
        self.client = app.test_client()
    
    def test_home_page(self):
        with self.client as client:
            res = client.get("/")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            # session items are created
            self.assertIn("board", session)
            self.assertIn("score", session)
            self.assertIn("played", session)
            # values are right
            self.assertEqual(session.get("score"), 0)
            self.assertEqual(session.get("played"), 0)
            # html template is correct
            self.assertIn('<span id="score">', html)
            self.assertIn('<span id="high-score">', html)
            self.assertIn('<span id="played">', html)
    
    def test_guess_word(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess["board"] = [
                    ["C", "A", "T", "T", "T"], 
                    ["C", "A", "T", "T", "T"], 
                    ["C", "A", "T", "T", "T"], 
                    ["C", "A", "T", "T", "T"], 
                    ["C", "A", "T", "T", "T"]
                ]
            res = client.get("/guess?word=cat")
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json["result"], "ok")
    
    def test_update_stats(self):
        with self.client as client:
            client.get("/")
            res = client.post("/update", json={"score": 6})
            self.assertEqual(res.json["played"], 1)
            self.assertAlmostEqual(res.json["score"], 6)
            self.assertEqual(session["played"], 1)
            # check if times played increases
            client.post("/update", json={"score": 6})
            self.assertEqual(session["played"], 2)
    
    def test_invalid_word(self):
        with self.client as client:
            client.get("/")
            res = client.get("/guess?word=impossible")
            self.assertEqual(res.json["result"], "not-on-board")
    
    def test_non_english_word(self):
        with self.client as client:
            client.get("/")
            res = client.get("/guess?word=eaigjlakgr")
            self.assertEqual(res.json["result"], "not-word")
    
