import numpy as np
from simx.blueprint import BluePrint
from simx.equation import Equation


class Sim:
    def __init__(self, blueprint: BluePrint):
        self.blueprint = blueprint
        self.progress = {var: [val] for var, val in self.blueprint.var_val_dict.items()}

    def step(self, time_step=1.0, min_val=-10.0, max_val=10.0):
        # TODO: numpyfy this

        # calculate dvar
        dvars = []
        for var in self.blueprint.all_vars:
            dvar = self.calculate_dvar(self.blueprint.get_equation(var))
            dvars.append(dvar)

        # update var
        for var, delta in tuple(zip(self.blueprint.all_vars, dvars)):
            self.blueprint.get_equation(var).lhs_val += delta * time_step
            self.blueprint.get_equation(var).lhs_val = max(
                min(self.blueprint.get_equation(var).lhs_val, max_val), min_val
            )
            self.progress[var].append(self.blueprint.get_equation(var).lhs_val)

    def run(self, num_step, time_step, min_clip, max_clip):
        for i in range(num_step):
            self.step(time_step, min_clip, max_clip)

    def calculate_dvar(self, equation: Equation):
        eles_transformed = []
        for i, ele in enumerate(equation.rhs):
            ele_val = self.blueprint.var_param_dict[ele]
            ele_transformed = self.apply_transform(ele_val, equation.transforms[i])
            eles_transformed.append(ele_transformed)

        dvar = 0
        for i, op in enumerate(["+"] + equation.ops):
            dvar = self.apply_op(dvar, eles_transformed[i], op)
        return dvar

    def apply_transform(self, val: float, transform: str):
        if transform == "log":
            return np.log(abs(val))
        elif transform == "sqrt":
            return np.sqrt(abs(val))
        elif transform == "exp":
            return np.exp(val)
        elif transform == "":
            return val

    def apply_op(self, val_1: float, val_2: float, op: str):
        if op == "+":
            return val_1 + val_2
        elif op == "-":
            return val_1 - val_2
        elif op == "*":
            return val_1 * val_2
        elif op == "/":
            return val_1 / val_2
        elif op == "**":
            if val_1 < 0 and val_2 < 1:
                return abs(val_1) ** val_2
            return val_1**val_2
