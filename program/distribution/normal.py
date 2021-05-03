from symengine.lib.symengine_wrapper import Expr, oo
from .distribution import Distribution
from .exceptions import EvaluationException
from scipy.stats import norm
import math


class Normal(Distribution):
    mu: Expr
    sigma2: Expr

    def set_parameters(self, parameters):
        if len(parameters) != 2:
            raise RuntimeError("Normal distribution requires 2 parameters")
        self.mu = parameters[0]
        self.sigma2 = parameters[1]

    def get_moment(self, k: int):
        #TODO
        pass

    def is_discrete(self):
        return False

    def subs(self, substitutions):
        self.mu = self.mu.subs(substitutions)
        self.sigma2 = self.sigma2.subs(substitutions)

    def sample(self, state):
        mu = self.mu.subs(state)
        sigma2 = self.sigma2.subs(state)
        if not mu.is_Number or not sigma2.is_Number:
            raise EvaluationException(f"Parameters {self.mu}, {self.sigma2} don't evaluate to numbers with state {state}")
        return norm.rvs(loc=float(mu), scale=math.sqrt(float(sigma2)))

    def get_free_symbols(self):
        return self.mu.free_symbols.union(self.sigma2.free_symbols)

    def get_support(self):
        return -oo, oo

    def __str__(self):
        return f"Normal({self.mu}, {self.sigma2})"
