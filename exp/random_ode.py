import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

import sys

sys.path.append(r"C:\Users\khoah\CovertLabProjects\SimExplainer")

from simx.config import Config
from simx.initializer import Initializer
from simx.blueprint import BluePrintGenerator
from simx.sim import Sim

random.seed(112)
np.random.seed(10)
n = 10
plt.figure(figsize=(10, 20))

for i in range(1, n):
    config = Config(
        param_num=5,
        var_num=5,
        param_each=i,
        var_each=i,
        transform_each=4,
        ops=["+", "-", "*", "/"],
    )
    initializer = Initializer(config, mu=0.0)
    gen = BluePrintGenerator(config)
    blueprint = gen.generate_blueprint(
        var_inits=initializer.var_inits,
        param_vals=initializer.param_vals,
        initializer=initializer,
    )
    sim = Sim(blueprint)
    sim.run(100, time_step=0.01, min_clip=-20.0, max_clip=20.0)
    df = pd.DataFrame(sim.progress)
    plt.subplot(n, 1, i)
    plt.title(f"N = {i}")
    sns.lineplot(df, legend=None)
    plt.ylim(-20, 20)
    print(blueprint.equations)

plt.show()
