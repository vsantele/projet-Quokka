from osmnx.routing import shortest_path
import osmnx as ox


def min_path(pos_from: tuple[float, float], pos_to: tuple[float, float]):
    weight = "length"
    G = ox.graph_from_point(
        (pos_from[0], pos_from[1]),
        dist=1200,
        dist_type="bbox",
        network_type="walk",
    )
    node_from = ox.nearest_nodes(G, pos_from[1], pos_from[0])
    node_to = ox.nearest_nodes(G, pos_to[1], pos_to[0])
    nodes = shortest_path(G, node_from, node_to, weight=weight)
    if nodes is None:
        return None
    polyline = [(G.nodes[node]["y"], G.nodes[node]["x"]) for node in nodes]
    return {
        "type": "Feature",
        "properties": {},
        "geometry": {"type": "LineString", "coordinates": polyline},
    }
