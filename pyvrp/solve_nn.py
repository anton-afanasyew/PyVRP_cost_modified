from collections import defaultdict
from pyvrp._pyvrp import (
    Client,
    Depot,
    ProblemData,
    VehicleType,
)
import numpy as np

def solve_nn(
        depot0: Depot, 
        clients: list[Client], 
        edges: list, 
        max_duration: int = np.iinfo(np.int64).max, 
        prize_weighted: bool = None
    ) -> list[str]:
    if len(clients) > 0:
        route_is_feasible: bool = True
        route_names: list = []
        duration: int = 0
        j = depot0
    else:
        print("There are no clients in Model")
        return []

    while route_is_feasible:
        edges_to_depot = defaultdict(int)
        edges_to_i = defaultdict(int)
        prizes_i = defaultdict(int)
        for edge in edges:
            if edge.to != edge.frm and (edge.frm == j or edge.to == depot0):
                if edge.to is Depot:
                    edges_to_depot[str(edge.frm)] = edge.duration
                else:
                    edges_to_i[str(edge.to)] = edge.duration + (j.service_duration if type(j) is not Depot else 0)
                    if prize_weighted:
                        prizes_i[str(edge.to)] = (edge.to.prize if type(edge.to) is not Depot else 0)
        edges_to_i = {key: value for key, value in edges_to_i.items() if (duration + value + edges_to_depot[key]) < max_duration}


        if edges_to_i:
            if prize_weighted:
                edges_to_i_weighted = {key: (value - prizes_i[key]) for key, value in edges_to_i.items() if (duration + value + edges_to_depot[key]) < max_duration}
            else:
                edges_to_i_weighted = edges_to_i
            
            i = next((client for client in clients if client.name == min(edges_to_i_weighted, key = edges_to_i_weighted.get)), None)
            route_names.append(i.name)
            duration += min(edges_to_i.values())
            duration += i.service_duration
            
            edges = [edge for edge in edges if edge.to != i and edge.frm != i] # delete edges from and to visited clients
            clients = [client for client in clients if client != i] # delete visited clients
        else:
            route_is_feasible = False
            break
    return route_names