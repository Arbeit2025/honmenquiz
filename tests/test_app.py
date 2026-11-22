# -*- coding: utf-8 -*-
"""honmenquiz の単体テスト（問題データの整合性とルート確認）。"""
import sys
import unittest
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import app as app_module

EXPECTED_CATEGORIES = {
    "法規の基礎", "標識・標示", "高速道路", "安全運転", "車両・応急・その他",
}


class TestQuestionData(unittest.TestCase):
    def test_exact_count(self):
        self.assertEqual(len(app_module.QUESTIONS), 120)

    def test_each_category_exactly_24(self):
        counts = Counter(q["category"] for q in app_module.QUESTIONS)
        self.assertEqual(set(counts.keys()), EXPECTED_CATEGORIES)
        for cat, n in counts.items():
            self.assertEqual(n, 24, cat)

    def test_all_fields_non_empty(self):
        for q in app_module.QUESTIONS:
            self.assertIsInstance(q["q"], str)
            self.assertTrue(q["q"].strip())
            self.assertIsInstance(q["answer"], bool)
            self.assertIsInstance(q["explanation"], str)
            self.assertTrue(q["explanation"].strip())
            self.assertIn(q["category"], EXPECTED_CATEGORIES)

    def test_no_duplicate_questions(self):
        texts = [q["q"] for q in app_module.QUESTIONS]
        self.assertEqual(len(texts), len(set(texts)))

    def test_answer_balance(self):
        total = len(app_module.QUESTIONS)
        true_count = sum(1 for q in app_module.QUESTIONS if q["answer"])
        ratio = true_count / total
        self.assertGreaterEqual(ratio, 0.40)
        self.assertLessEqual(ratio, 0.60)


class TestRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app_module.app.test_client()

    def test_index_ok(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        body = resp.get_data(as_text=True)
        self.assertIn("本免対策 ○×カード", body)
        self.assertIn("イラスト問題", body)

    def test_healthz(self):
        resp = self.client.get("/healthz")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json(), {"status": "ok"})

    def test_api_questions(self):
        resp = self.client.get("/api/questions")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(len(data), 120)
        self.assertEqual(data[0]["category"], "法規の基礎")
        self.assertIn("explanation", data[0])


if __name__ == "__main__":
    unittest.main()
