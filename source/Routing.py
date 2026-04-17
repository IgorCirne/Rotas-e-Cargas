from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import random
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import networkx as nx
import Cargas


# All data model is using dummy data, but most of it should be hard-coded for performance
def create_data_model():
    # Stores the data for the problem.
    # Also imports Cargas to use optimized loads for each vehicle
    # Cargas still generates dummy data
    
    data = {}
    optimized_weights = Cargas.get_optimized_loads(num_vehicles=5)
    
    # The distance matrix works as follows: each line is related to a singular location, the number in the index is the distance of the original location to the respective location
    # For example: The following matrix has 17 locations, on the index 1-4, you can see the distance from location 1 to location 4, as it can be observed, the main diagonal is 0
    # Because the location's distance to itself is null.
    # The matrix should be always hard-coded, if not, the program will take ages to run
    data["distance_matrix"] = [
        # Distance should be hard-coded between the 17 deposits, unless you hate performance
        [0, 548, 776, 696, 582, 274, 502, 194, 308, 194, 536, 502, 388, 354, 468, 776, 662],
        [548, 0, 684, 308, 194, 502, 730, 354, 696, 742, 1084, 594, 480, 674, 1016, 868, 1210],
        [776, 684, 0, 992, 878, 502, 274, 810, 468, 742, 400, 1278, 1164, 1130, 788, 1552, 754],
        [696, 308, 992, 0, 114, 650, 878, 502, 844, 890, 1232, 514, 628, 822, 1164, 560, 1358],
        [582, 194, 878, 114, 0, 536, 764, 388, 730, 776, 1118, 400, 514, 708, 1050, 674, 1244],
        [274, 502, 502, 650, 536, 0, 228, 308, 194, 240, 582, 776, 662, 628, 514, 1050, 708],
        [502, 730, 274, 878, 764, 228, 0, 536, 194, 468, 354, 1004, 890, 856, 514, 1278, 480],
        [194, 354, 810, 502, 388, 308, 536, 0, 342, 388, 730, 468, 354, 320, 662, 742, 856],
        [308, 696, 468, 844, 730, 194, 194, 342, 0, 274, 388, 810, 696, 662, 320, 1084, 514],
        [194, 742, 742, 890, 776, 240, 468, 388, 274, 0, 342, 536, 422, 388, 274, 810, 468],
        [536, 1084, 400, 1232, 1118, 582, 354, 730, 388, 342, 0, 878, 764, 730, 388, 1152, 354],
        [502, 594, 1278, 514, 400, 776, 1004, 468, 810, 536, 878, 0, 114, 308, 650, 274, 844],
        [388, 480, 1164, 628, 514, 662, 890, 354, 696, 422, 764, 114, 0, 194, 536, 388, 730],
        [354, 674, 1130, 822, 708, 628, 856, 320, 662, 388, 730, 308, 194, 0, 342, 422, 536],
        [468, 1016, 788, 1164, 1050, 514, 514, 662, 320, 274, 388, 650, 536, 342, 0, 764, 194],
        [776, 868, 1552, 560, 674, 1050, 1278, 742, 1084, 810, 1152, 274, 388, 422, 764, 0, 798],
        [662, 1210, 754, 1358, 1244, 708, 480, 856, 514, 468, 354, 844, 730, 536, 194, 798, 0],

    ]
    # Demands for each of the places, as it stands, demand is based on weight
    data["demands"] = [0, 1, 1, 3, 6, 3, 6, 10, 8, 1, 2, 1, 2, 6, 6, 6, 8]
    data["vehicle_capacities"] = optimized_weights
    data["num_vehicles"] = len(optimized_weights)
    data["depot"] = 0
    data["coordinates"] = generate_coordinates(len(data["distance_matrix"]))

    return data

def generate_coordinates(n):
    return [(random.randint(0, 100), random.randint(0, 100)) for _ in range(n)]

def get_routes(data, manager, routing, assignment):
    routes = []

    for vehicle_id in range(data["num_vehicles"]):
        if not routing.IsVehicleUsed(assignment, vehicle_id):
            continue

        index = routing.Start(vehicle_id)
        route = []

        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            route.append(node)
            index = assignment.Value(routing.NextVar(index))

        route.append(manager.IndexToNode(index))
        routes.append(route)

    return routes

def plot_routes(data, routes):
    G = nx.DiGraph()
    coords = data["coordinates"]

    for i, (x, y) in enumerate(coords):
        G.add_node(i, pos=(x, y))

    pos = nx.get_node_attributes(G, 'pos')

    plt.figure(figsize=(10, 8))

    colors = ["red", "blue", "green", "purple", "orange", "brown"]
    legend_elements = []

    for i, route in enumerate(routes):
        color = colors[i % len(colors)]


        edges = [(route[j], route[j+1]) for j in range(len(route)-1)]

        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=edges,
            edge_color=color,
            width=2,
            arrows=True,
            arrowstyle='-|>',
            arrowsize=20
        )

        legend_elements.append(
            Line2D([0], [0], color=color, lw=2, label=f'Caminhão {i+1}')
        )

    # Nós
    nx.draw_networkx_nodes(G, pos, node_size=300)
    nx.draw_networkx_labels(G, pos)

    # Destacar depósito
    nx.draw_networkx_nodes(G, pos, nodelist=[0], node_color='yellow', node_size=500)

    plt.legend(handles=legend_elements)
    plt.title("Rotas dos Caminhões (CVRP - Direcionado)")
    plt.show()

def preprocess_data(data):
    max_capacity = max(data["vehicle_capacities"])

    valid_nodes = []

    # Always keep depot on nodes
    valid_nodes.append(0)

    # Filtrar nós válidos
    for i in range(1, len(data["demands"])):
        if data["demands"][i] <= max_capacity:
            valid_nodes.append(i)
        else:
            print(f"Removendo nó {i} (demanda {data['demands'][i]} > capacidade máxima)")

    # Filtered distance matrix
    new_matrix = []
    for i in valid_nodes:
        row = []
        for j in valid_nodes:
            row.append(data["distance_matrix"][i][j])
        new_matrix.append(row)

    # Create new demands
    new_demands = [data["demands"][i] for i in valid_nodes]

    # Update data
    data["distance_matrix"] = new_matrix
    data["demands"] = new_demands

    return data

def print_solution(data, manager, routing, assignment):
    # Prints assignment on console.
    print(f"Objective: {assignment.ObjectiveValue()}\n")
    # Display dropped nodes.
    dropped_nodes = "Dropped nodes:"
    for node in range(routing.Size()):
        if routing.IsStart(node) or routing.IsEnd(node):
            continue
        if assignment.Value(routing.NextVar(node)) == node:
            dropped_nodes += f" {manager.IndexToNode(node)}"
    print(dropped_nodes)
    print("\n")
    # Display routes
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data["num_vehicles"]):
        if not routing.IsVehicleUsed(assignment, vehicle_id):
            continue
        index = routing.Start(vehicle_id)
        plan_output = f"Route for truck {vehicle_id}:\n"
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data["demands"][node_index]
            plan_output += f" {node_index} Load({route_load}) -> "
            previous_index = index
            index = assignment.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
        plan_output += f" {manager.IndexToNode(index)} Load({route_load})\n"
        plan_output += f"Distance of the route: {route_distance}m\n"
        plan_output += f"Load of the route: {route_load}\n"
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
    print(f"Total Distance of all routes: {total_distance}m")
    print(f"Total Load of all routes: {total_load}")


def main():
    # Solve the CVRP problem.
    # Instantiate the data problem.
    data = create_data_model()

    data = preprocess_data(data)
    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        # Returns the distance between the two nodes.
        # Convert from routing variable Index to distance matrix Node Index.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Capacity constraint.
    def demand_callback(from_index):
        # Returns the demand of the node.
        # Convert from routing variable Index to demands Node Index.
        from_node = manager.IndexToNode(from_index)
        return data["demands"][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data["vehicle_capacities"],  # vehicle maximum capacities
        True,  # start cumul to zero
        "Capacity",
    )
    # Allow to drop nodes.
    penalty = sum(max(row) for row in data["distance_matrix"])
    # penalty = max(data["distance_matrix"] * 10)
    for node in range(len(data["distance_matrix"])):
        if node == data["depot"]:
            continue
        routing.AddDisjunction([node], penalty)

    # Setting first solution heuristic. I am using the cheapest path metric as a baseline
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.SAVINGS
    )
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_parameters.guided_local_search_lambda_coefficient = 0.1

    search_parameters.time_limit.FromSeconds(20) # set time limit to 20 seconds

    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if assignment:
        print_solution(data, manager, routing, assignment)

        # gerar e plotar rotas
        routes = get_routes(data, manager, routing, assignment)
        plot_routes(data, routes)


if __name__ == "__main__":
    main()
