import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_selection import mutual_info_regression


def plot_sim(sim):
    df = pd.DataFrame(sim.progress)
    plt.figure(figsize=(10, 10))
    plt.subplot(n, 1, i)
    plt.title(f"N = {i}")
    sns.lineplot(df)
    plt.ylim(-20, 20)
    plt.show()


def diff_sim(sim1, sim2):
    diff = pd.DataFrame(sim1.progress) - pd.DataFrame(sim2.progress)
    plt.figure(figsize=(10, 10))
    plt.subplot(n, 1, i)
    plt.title(f"N = {i}")
    sns.lineplot(diff, legend=None)
    plt.ylim(-20, 20)
    plt.show()
    print(diff.abs().sum(axis=0))


def mutual_information(a, b):
    a = a.reshape(-1, 1)
    b = b.reshape(-1, 1).ravel()
    return mutual_info_regression(a, b)[0]
