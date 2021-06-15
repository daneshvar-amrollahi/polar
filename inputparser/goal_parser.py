from .exceptions import ParseException
from symengine.lib.symengine_wrapper import sympify
import re

MOMENT = "MOMENT"
TAIL_BOUND_UPPER = "TAIL_BOUND_UPPER"
TAIL_BOUND_LOWER = "TAIL_BOUND_LOWER"


class GoalParser:

    @staticmethod
    def parse(goal: str):
        if len(goal) < 4:
            raise ParseException(f"Malformed goal {goal}")

        if goal[0] == "E":
            return GoalParser.__parse_moment__(goal)
        if goal[0] == "P":
            return GoalParser.__parse_tail_bound__(goal)
        raise ParseException(f"Unknown goal {goal}")

    @staticmethod
    def __parse_moment__(goal: str):
        if goal[1] != "(" or goal[-1] != ")":
            raise ParseException(f"Malformed goal {goal}")
        between_brackets = goal[2:-1].strip()
        return MOMENT, [sympify(between_brackets)]

    @staticmethod
    def __parse_tail_bound__(goal: str):
        match = re.search("^P\\(([0-9a-zA-Z*/.+\\-)( ]*?)>=([0-9a-zA-Z*/.+\\-)( ]*?)\\)( )*<=( )*\\?( )*", goal)
        if match:
            return TAIL_BOUND_UPPER, [sympify(t) for t in [match.group(1), match.group(2)]]

        match = re.search("^P\\(([0-9a-zA-Z*/.+\\-)( ]*?)>([0-9a-zA-Z*/.+\\-)( ]*?)\\)( )*>=( )*\\?( )*", goal)
        if match:
            return TAIL_BOUND_LOWER, [sympify(t) for t in [match.group(1), match.group(2)]]

        raise ParseException(f"Unknown goal {goal}")
