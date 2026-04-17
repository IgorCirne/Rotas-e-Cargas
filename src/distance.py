import osmnx as ox
import matplotlib
import matplotlib.pyplot as plt

# Using TkAgg to avoid problems
matplotlib.use('TkAgg')

# Start and finish coordinates
orig = (-4.9582253, -37.1316916)
dest = (-5.153807, -37.3594689)


G = ox.graph_from_point(orig, dist=1000, network_type='drive')

# Adding speed and travel time properties
# G = ox.routing.add_edge_speeds(G)
# G = ox.routing.add_edge_travel_times(G)

orig_node = ox.distance.nearest_nodes(G, orig[1], orig[0])
dest_node = ox.distance.nearest_nodes(G, dest[1], dest[0])

# Calculating shortest route using OX
route = ox.shortest_path(G, orig_node, dest_node, weight='travel_time')

# Using GDF to obtain the total distance in meters, it can easily be converted to KM
route_gdf = ox.routing.route_to_gdf(G, route)
total_distance_m = route_gdf['length'].sum()
# total_time_s = route_gdf['travel_time'].sum()

print(f"Total distance: {total_distance_m:.2f} meters")
# print(f"Estimated time: {total_time_s:.2f} seconds")

# Plotting the map
fig, ax = ox.plot_graph_route(G, route, node_size=30, show=False, close=False, figsize=(10, 10))

# Adding markers for origin and end
padding = 0
ax.scatter(orig[1], orig[0], c='lime', s=200, label='origin', marker='x')
ax.scatter(dest[1], dest[0], c='red', s=200, label='end', marker='x')
ax.set_ylim([min(orig[0], dest[0]) - padding, max(orig[0], dest[0]) + padding])
ax.set_xlim([min(orig[1], dest[1]) - padding, max(orig[1], dest[1]) + padding])

plt.legend()
plt.show()
