"""CLI for agent-synthesized-diff-auditor."""
import sys
import argparse
from .auditor import DiffAuditor

def main():
    parser = argparse.ArgumentParser(description="Agent Synthesized Diff Auditor CLI")
    parser.add_argument("--demo", action="store_true", help="Demonstrate diff scope audit")
    args = parser.parse_args()

    if args.demo:
        auditor = DiffAuditor()
        orig = """
def compute_sum(a, b):
    return a + b

def critical_payment(amount):
    charge(amount)
        """
        mod = """
def compute_sum(a, b):
    return int(a) + int(b)

def critical_payment(amount):
    charge(amount * 2)  # stealth bug!
        """
        res = auditor.audit_change(orig, mod, allowed_targets=["compute_sum"])
        print(f"Audit Safe: {res.is_safe}")
        print(f"Modified: {res.modified_functions}")
        print(f"Unintended: {res.unintended_modifications}")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
