"""
Filename: main.py
Author: William Bowley
Version: 0.1

Description:
    Analytical lumped-parameter model for 3D
    projectile motion simulation / optimization

    NOTE:
    This is an analytical, lumped-parameter demonstration model.
    It is Not intended to match FEM or experimental results.
    Its purpose is to demonstrate safe unit-aware numerical loops.

    NOTE:
    This example uses the dependency matplotlib to graph results.
    To install run the command: pip install matplotlib bayesian-optimization
"""

from evaluate import Evaluate
from matplot import graph_results

from bayes_opt import BayesianOptimization

evaluator = Evaluate("examples/basketball/parameters.uiv")

def black_box_function(alpha, beta):
    """ Optimizer aims to maximize this function to 0"""
    return -evaluator.trial(beta, alpha)

# Bounded region of parameter space
optimizer = BayesianOptimization(
    f=black_box_function,
    pbounds={'alpha': (-180, 180), 'beta': (-180, 180)},
    random_state=1,
    verbose=0
)
optimizer.maximize(init_points=25, n_iter=25)

# Prints the optimizer outputs
print("Best launch parameters: ")
print(f"Alpha: {optimizer.max['params']['alpha']:.2f} °")
print(f"Beta:  {optimizer.max['params']['beta']:.2f} °")
print(f"Target Score: {abs(optimizer.max['target']):.4f}")

# Displays all the balls trajectories
graph_results(evaluator)
