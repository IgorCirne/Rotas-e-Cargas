from ortools.algorithms.python import knapsack_solver
from ortools.linear_solver import pywraplp
import random



# Initializing the variables of the loads which are going into the routing problem
def init_load(load, num_vehicles):
    num_items = 50

    load["weights"] = [0] * num_items
    load["volumes"] = [0] * num_items
    load["values"] = [0] * num_items

    init_weights(load, num_items)
    init_volumes(load)
    init_values(load, num_items)

    assert len(load["weights"]) == len(load["values"])

    load["num_items"] = num_items
    load["all_items"] = range(num_items)
    load["truck_max_weight"] = [15] * num_vehicles
    load["volume_capacity"] = [15] * num_vehicles
    load["num_trucks"] = num_vehicles
    load["all_bins"] = range(num_vehicles)

    return load


# Creating functions to initalize the keys to the loads directory

def init_weights(load, num_items):
    load["weights"] = [random.randint(1, 10) for _ in range(num_items)]


def init_volumes(load):
    load["volumes"] = [
        int(weight * random.uniform(0.8, 1.2)) if weight > 0 else random.randint(1, 10)
        for weight in load["weights"]
    ]


def init_values(load, num_items):
    load["values"] = [random.randint(0, 500) for _ in range(num_items)]

# function which optimizes the loads based on merchandise value
def get_optimized_loads(num_vehicles=5, num_items=50):
    load = {}
    init_load(load, num_vehicles)

    solver = pywraplp.Solver.CreateSolver("SCIP")
    if solver is None:
        raise RuntimeError("SCIP solver unavailable.")

    # Setting the constraints of the problem
    x = {}
    for i in load["all_items"]:
        for b in load["all_bins"]:
            x[i, b] = solver.BoolVar(f"x_{i}_{b}")

    for i in load["all_items"]:
        solver.Add(sum(x[i, b] for b in load["all_bins"]) <= 1)

    for b in load["all_bins"]:
        solver.Add(
            sum(x[i, b] * load["weights"][i] for i in load["all_items"])
            <= load["truck_max_weight"][b]
        )
        solver.Add(
            sum(x[i, b] * load["volumes"][i] for i in load["all_items"])
            <= load["volume_capacity"][b]
        )

    objective = solver.Objective()
    for i in load["all_items"]:
        for b in load["all_bins"]:
            objective.SetCoefficient(x[i, b], load["values"][i])
    objective.SetMaximization()

    print(f"Solving with {solver.SolverVersion()}")
    status = solver.Solve()

    optimized_weights = []

    if status == pywraplp.Solver.OPTIMAL:
        
        print_optimized_loads_result(load, x) # <-- This line exists solely to print the results, and can be commented/removed if performance is an issue

        for b in load["all_bins"]:
            bin_weight = sum(
                load["weights"][i]
                for i in load["all_items"]
                if x[i, b].solution_value() > 0
            )
            optimized_weights.append(bin_weight)
    else:
        print("The problem does not have an optimal solution.")

    return optimized_weights

# Function to print results, called in the optimized loadouts function
def print_optimized_loads_result(load, x):
    total_weight = 0
    total_value = 0
    total_volume = 0

    for b in load["all_bins"]:
        print(f"Truck {b+1}")
        bin_weight = 0
        bin_value = 0
        bin_volume = 0
        for i in load["all_items"]:
            if x[i, b].solution_value() > 0:
                print(
                    f"Item {i} weight: {load['weights'][i]} value: {load['values'][i]}"
                )
                bin_weight += load["weights"][i]
                bin_value += load["values"][i]
                bin_volume += load["volumes"][i]
        print(f"Packed bin weight: {bin_weight}")
        print(f"Packed bin value: {bin_value}")
        print(f"Packed bin volume: {bin_volume}\n")
        total_weight += bin_weight
        total_value += bin_value
        total_volume += bin_volume

    print(f"Total packed weight: {total_weight}")
    print(f"Total packed value: {total_value}")
    print(f"Total packed volume: {total_volume}\n\n")
    print(f"------------------------------------------------------------------\n\n") # <-- This line exists only to help in formatting

if __name__ == "__main__":
    get_optimized_loads(num_vehicles=5, num_items=50)



