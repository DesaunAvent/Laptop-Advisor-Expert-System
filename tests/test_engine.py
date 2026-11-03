
import unittest
import sys
import os

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from engine import ForwardChainingEngine
from kb_loader import load_rules


class TestLaptopAdvisor(unittest.TestCase):

    def setUp(self):
        kb_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "kb",
            "laptop_rules.json"
        )
        self.rules = load_rules(kb_path)

    def run_engine(self, facts):
        engine = ForwardChainingEngine(self.rules)
        engine.assert_facts(facts)
        engine.run()
        return engine.conclusions()

    def test_premium_ultrabook(self):
        facts = ["budget_high", "portable", "long_battery"]
        results = self.run_engine(facts)

        self.assertIn(
            "recommend:premium_ultrabook",
            results["recommendations"]
        )

    def test_budget_ultrabook(self):
        facts = ["budget_low", "office_only", "portable"]
        results = self.run_engine(facts)

        self.assertIn(
            "recommend:budget_ultrabook",
            results["recommendations"]
        )

    def test_gaming_laptop(self):
        facts = ["gaming", "budget_medium"]
        results = self.run_engine(facts)

        self.assertIn(
            "recommend:midrange_gaming_laptop",
            results["recommendations"]
        )

    def test_high_end_gaming(self):
        facts = ["gaming", "budget_high"]
        results = self.run_engine(facts)

        self.assertIn(
            "recommend:high_end_gaming_laptop",
            results["recommendations"]
        )

    def test_creative_work(self):
        facts = ["creative_work", "portable"]
        results = self.run_engine(facts)

        self.assertIn(
            "spec:ram_16_plus",
            results["specs"]
        )

    def test_linux(self):
        facts = ["pref_os_linux", "office_only"]
        results = self.run_engine(facts)

        self.assertIn(
            "spec:linux_friendly_hw",
            results["specs"]
        )


if __name__ == "__main__":
    unittest.main()
