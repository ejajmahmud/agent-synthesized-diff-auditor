"""Unit tests for agent-synthesized-diff-auditor."""
import unittest
from agent_synthesized_diff_auditor.auditor import DiffAuditor

class TestDiffAuditor(unittest.TestCase):
    def setUp(self):
        self.auditor = DiffAuditor()

    def test_contained_change_is_safe(self):
        c1 = "def fn_a(): return 1\ndef fn_b(): return 2"
        c2 = "def fn_a(): return 100\ndef fn_b(): return 2"
        res = self.auditor.audit_change(c1, c2, allowed_targets=["fn_a"])
        self.assertTrue(res.is_safe)
        self.assertEqual(res.modified_functions, {"fn_a"})

    def test_unintended_change_flagged(self):
        c1 = "def fn_a(): return 1\ndef fn_b(): return 2"
        c2 = "def fn_a(): return 100\ndef fn_b(): return 999"
        res = self.auditor.audit_change(c1, c2, allowed_targets=["fn_a"])
        self.assertFalse(res.is_safe)
        self.assertIn("fn_b", res.unintended_modifications)
