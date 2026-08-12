"""Safe formula evaluation engine for unit conversions.
Supports Excel-style formulas without arbitrary code execution.
"""
import re
import operator
import math
from decimal import Decimal, InvalidOperation
from typing import Dict, Any

class FormulaError(Exception):
    pass

class FormulaEngine:
    """Safe formula parser and evaluator for unit conversions.
    
    Supported syntax:
    - Numbers: 12, 0.5, 2.5
    - Operators: +, -, *, /, ^
    - Parentheses: ( )
    - Unit references: PCS, KG, BOX (resolved via context)
    - Functions: ROUND, SQRT
    """
    
    TOKEN_SPEC = [
        ("NUMBER", r"\d+(?:\.\d+)?"),
        ("NAME", r"[A-Za-z_][A-Za-z0-9_]*"),
        ("OP", r"[+\-*/^()]"),
        ("SKIP", r"[ \t]+"),
        ("MISMATCH", r"."),
    ]
    
    TOKEN_RE = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC))
    
    @classmethod
    def tokenize(cls, formula: str):
        text = formula.strip().lstrip("=").strip()
        tokens = []
        for mo in cls.TOKEN_RE.finditer(text):
            kind = mo.lastgroup
            value = mo.group()
            if kind == "SKIP":
                continue
            elif kind == "MISMATCH":
                raise FormulaError(f"Unexpected character: {value}")
            tokens.append((kind, value))
        return tokens
    
    @classmethod
    def validate_syntax(cls, formula: str):
        tokens = cls.tokenize(formula)
        # Check parentheses balance
        parens = sum(1 for t in tokens if t[1] == "(") - sum(1 for t in tokens if t[1] == ")")
        if parens != 0:
            raise FormulaError("Unbalanced parentheses")
        # Check no consecutive operators (basic)
        ops = {"+", "-", "*", "/", "^"}
        for i in range(len(tokens) - 1):
            if tokens[i][1] in ops and tokens[i+1][1] in ops:
                if tokens[i+1][1] not in {"+", "-"}:  # unary allowed after operator
                    raise FormulaError(f"Consecutive operators: {tokens[i][1]} {tokens[i+1][1]}")
        return True
    
    @classmethod
    def evaluate(cls, formula: str, unit_values: Dict[str, Decimal]) -> Decimal:
        """Evaluate formula with given unit values.
        
        Example:
            formula = "=12*PCS"
            unit_values = {"PCS": Decimal("1")}
            result = Decimal("12")
        """
        cls.validate_syntax(formula)
        tokens = cls.tokenize(formula)
        
        # Convert to postfix (RPN) using shunting yard
        output = []
        stack = []
        precedence = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
        
        i = 0
        while i < len(tokens):
            kind, value = tokens[i]
            if kind == "NUMBER":
                output.append(Decimal(value))
            elif kind == "NAME":
                upper_val = value.upper()
                if upper_val in unit_values:
                    output.append(unit_values[upper_val])
                elif upper_val == "ROUND":
                    stack.append("ROUND")
                elif upper_val == "SQRT":
                    stack.append("SQRT")
                else:
                    raise FormulaError(f"Unknown reference: {value}")
            elif value == ",":
                while stack and stack[-1] != "(":
                    output.append(stack.pop())
            elif value == "(":
                stack.append(value)
            elif value == ")":
                while stack and stack[-1] != "(":
                    output.append(stack.pop())
                if not stack:
                    raise FormulaError("Mismatched parentheses")
                stack.pop()  # pop "("
                if stack and stack[-1] in {"ROUND", "SQRT"}:
                    output.append(stack.pop())
            elif kind == "OP":
                while (stack and stack[-1] != "(" and
                       stack[-1] in precedence and
                       precedence[stack[-1]] >= precedence.get(value, 0)):
                    output.append(stack.pop())
                stack.append(value)
            i += 1
        
        while stack:
            op = stack.pop()
            if op in {"(", ")"}:
                raise FormulaError("Mismatched parentheses")
            output.append(op)
        
        # Evaluate RPN
        eval_stack = []
        for token in output:
            if isinstance(token, Decimal):
                eval_stack.append(token)
            elif token == "+":
                b, a = eval_stack.pop(), eval_stack.pop()
                eval_stack.append(a + b)
            elif token == "-":
                b, a = eval_stack.pop(), eval_stack.pop()
                eval_stack.append(a - b)
            elif token == "*":
                b, a = eval_stack.pop(), eval_stack.pop()
                eval_stack.append(a * b)
            elif token == "/":
                b, a = eval_stack.pop(), eval_stack.pop()
                if b == 0:
                    raise FormulaError("Division by zero")
                eval_stack.append(a / b)
            elif token == "^":
                b, a = eval_stack.pop(), eval_stack.pop()
                eval_stack.append(a ** b)
            elif token == "ROUND":
                a = eval_stack.pop()
                eval_stack.append(a.quantize(Decimal("0.01")))
            elif token == "SQRT":
                a = eval_stack.pop()
                eval_stack.append(Decimal(str(math.sqrt(float(a)))))
        
        if len(eval_stack) != 1:
            raise FormulaError("Invalid formula expression")
        return eval_stack[0]


def validate_conversion_formula(formula: str, available_units: list[str]) -> dict:
    """Validate a unit conversion formula.
    
    Returns:
        {"valid": bool, "error": str|None, "normalized": str}
    """
    try:
        FormulaEngine.validate_syntax(formula)
        tokens = FormulaEngine.tokenize(formula)
        refs = {t[1].upper() for t in tokens if t[0] == "NAME"}
        funcs = {"ROUND", "SQRT"}
        unknown = refs - set(u.upper() for u in available_units) - funcs
        if unknown:
            return {"valid": False, "error": f"Unknown unit reference: {', '.join(unknown)}", "normalized": None}
        normalized = formula.strip().lstrip("=").strip().upper()
        return {"valid": True, "error": None, "normalized": normalized}
    except FormulaError as e:
        return {"valid": False, "error": str(e), "normalized": None}
