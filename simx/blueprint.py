from itertools import product
from copy import deepcopy
import random
import numpy as np
import matplotlib.pyplot as plt

import networkx as nx


from simx.equation import Equation
from simx.config import Config


class BluePrint:
    def __init__(
        self, equations: Equation, param_vals: dict, var_inits: dict, initializer=None
    ):
        self.equations = equations
        self.param_vals = param_vals
        self.var_inits = var_inits
        self.graph = self.build_graph()
        self.initializer = initializer

    @property
    def all_vars(self):
        return list(self.var_inits.keys())

    @property
    def all_params(self):
        return list(self.param_vals.keys())

    @property
    def var_val_dict(self):
        return {equation.lhs: equation.lhs_val for equation in self.equations}

    @property
    def var_param_dict(self):
        return {**self.var_val_dict, **self.param_vals}

    def reinit(self, var_inits):
        self.var_inits = var_inits
        for equation in self.equations:
            equation.lhs_val = self.var_inits[equation.lhs]

    def get_equation(self, var):
        for equation in self.equations:
            if equation.lhs == var:
                return equation

    def mutate(self, param, val=None):
        if val:
            self.param_vals[param] = val
        elif self.initializer:
            self.param_vals[param] = self.initializer.sample()
        else:
            self.param_vals[param] = 0

    def build_graph(self):
        G = nx.DiGraph()
        edges = []
        for eq in self.equations:
            edges.extend(product(eq.rhs, [eq.lhs]))
        G.add_edges_from(edges)
        return G

    def view_graph(self, param_views="all"):
        graph_view = deepcopy(self.graph)
        if isinstance(param_views, list):
            all_nodes = deepcopy(graph_view.nodes)
            for node in all_nodes:
                if "var" not in node and node not in param_views:
                    graph_view.remove_node(node)

        pos = nx.spring_layout(graph_view, seed=42)
        nx.draw(graph_view, pos, with_labels=True, node_size=50, node_color="skyblue")
        labels = nx.get_edge_attributes(graph_view, "weight")
        nx.draw_networkx_edge_labels(graph_view, pos, edge_labels=labels)
        plt.show()


class BluePrintGenerator:
    def __init__(self, config: Config):
        self.config = config

    def generate_rhs(self):
        rhs_vars = np.random.choice(
            self.config.variables, size=self.config.var_each, replace=True
        )
        rhs_params = np.random.choice(
            self.config.params, size=self.config.param_each, replace=True
        )
        rhs = list(rhs_vars) + list(rhs_params)
        random.shuffle(rhs)
        return rhs

    def generate_ops(self, rhs):
        operations = np.random.choice(self.config.ops, size=len(rhs) - 1, replace=True)
        return list(operations)

    def generate_transforms(self, rhs):
        transform_standardized = ["" for i in range(len(rhs))]
        transformations = list(
            np.random.choice(
                self.config.transforms, size=self.config.transform_each, replace=True
            )
        )
        transform_index = list(
            np.random.choice(
                range(len(rhs)), size=self.config.transform_each, replace=True
            )
        )
        for index in transform_index:
            transform_standardized[index] = transformations.pop()
        return transform_standardized

    def generate_blueprint(
        self, param_vals: dict = {}, var_inits: dict = {}, initializer=None
    ):
        self.equations = []
        if not any(var_inits):
            var_inits = self.config.var_inits
        else:
            assert var_inits.keys() == self.config.var_inits.keys()
        if not any(param_vals):
            param_vals = self.config.param_vals
        else:
            assert param_vals.keys() == self.config.param_vals.keys()

        for var in self.config.variables:
            rhs = self.generate_rhs()
            ops = self.generate_ops(rhs)
            transforms = self.generate_transforms(rhs)
            equation = Equation(
                lhs=var, lhs_val=var_inits[var], rhs=rhs, ops=ops, transforms=transforms
            )
            self.equations.append(equation)
        return BluePrint(self.equations, param_vals, var_inits, initializer)
