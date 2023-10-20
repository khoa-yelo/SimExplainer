import numpy as np
from simx.config import Config


class Initializer:
    def __init__(self, config: Config, mode="normal", mu=0.0, sigma=1.0):
        self.config = config
        self.var_inits = self.config.var_inits
        self.param_vals = self.config.param_vals
        self.mu = mu
        self.sigma = sigma

        if mode == "normal":
            self.sampler = np.random.normal
        for key, val in self.config.var_inits.items():
            sample = self.sampler(self.mu, self.sigma, 1)
            self.var_inits[key] = sample[0]

        for key, val in self.config.param_vals.items():
            sample = self.sampler(self.mu, self.sigma, 1)
            self.param_vals[key] = sample[0]

    def sample(self):
        return self.sampler(self.mu, self.sigma, 1)[0]
