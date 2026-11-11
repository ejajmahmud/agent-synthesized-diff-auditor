"""Core Diff Auditor implementation."""
import ast
from dataclasses import dataclass
from typing import Dict, List, Set

@dataclass
class AuditResult:
    is_safe: bool
    modified_functions: Set[str]
    unintended_modifications: Set[str]
    details: List[str]

class DiffAuditor:
    """Verifies that code edits only touch explicitly declared target functions."""
    
    def extract_function_sources(self, code: str) -> Dict[str, str]:
        tree = ast.parse(code)
        funcs = {}
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                funcs[node.name] = ast.unparse(node)
        return funcs

    def audit_change(self, original_code: str, modified_code: str, allowed_targets: List[str]) -> AuditResult:
        orig_funcs = self.extract_function_sources(original_code)
        mod_funcs = self.extract_function_sources(modified_code)

        modified_set = set()
        unintended_set = set()
        details = []
        allowed_set = set(allowed_targets)

        # Check existing and new functions
        all_func_names = set(orig_funcs.keys()).union(mod_funcs.keys())
        for f in all_func_names:
            src_orig = orig_funcs.get(f)
            src_mod = mod_funcs.get(f)

            if src_orig != src_mod:
                modified_set.add(f)
                if f not in allowed_set:
                    unintended_set.add(f)
                    details.append(f"Function '{f}' was modified but was NOT in the allowed target list: {allowed_targets}")

        is_safe = len(unintended_set) == 0
        if is_safe:
            details.append(f"All changes strictly contained within allowed target functions: {list(modified_set)}")

        return AuditResult(
            is_safe=is_safe,
            modified_functions=modified_set,
            unintended_modifications=unintended_set,
            details=details
        )
