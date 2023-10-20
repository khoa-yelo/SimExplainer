class Equation:
    def __init__(
        self, lhs: str, rhs: list, ops: list, transforms, lhs_val: float = 0.0
    ):
        self.lhs_val = lhs_val
        self.lhs = lhs
        self.rhs = rhs
        self.ops = ops
        self.transforms = transforms

    def __str__(self):
        pass

    def __repr__(self):
        equation_str = ""
        padded_ops = self.ops + [" END"]
        for i in range(len(self.rhs)):
            equation_str += self.transforms[i] + self.rhs[i] + padded_ops[i]
        return f"{self.lhs} =  {equation_str}"
