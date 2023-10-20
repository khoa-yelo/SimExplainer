class Config:
    def __init__(
        self,
        param_num: int,
        var_num: int,
        param_each: int,
        var_each: int,
        transform_each: int,
        var_inits: dict = {},
        param_vals: dict = {},
        ops: list = ["+", "-", "*", "/", "**"],
        transforms: list = ["exp", "log", "sqrt"],
    ):
        self.param_num = param_num
        self.var_num = var_num
        self.param_each = param_each
        self.var_each = var_each
        self.transform_each = transform_each
        if any(var_inits):
            assert list(var_inits.keys()) == self.variables
            self.var_inits = var_inits
        else:
            self.var_inits = {var: 1.0 for var in self.variables}
        if any(var_inits):
            assert list(param_vals.keys()) == self.params
            self.param_vals = param_vals
        else:
            self.param_vals = {param: 1.0 for param in self.params}
        self.ops = ops
        self.transforms = transforms

    @property
    def params(self):
        return [f"param_{i}" for i in range(self.param_num)]

    @property
    def variables(self):
        return [f"var_{i}" for i in range(self.var_num)]
