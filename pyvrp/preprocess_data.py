import yaml
import numpy as np

def from_config_int(section: str = None, default: int = None) -> int:
    '''
    Returns integer parameters from config.yaml file
    
    section: str = None
    default: int = None
    '''
    with open("config.yaml", 'r') as file:
        config = yaml.safe_load(file)
    if section is None:
        return default
    try:
        return int(config[section])
    except KeyError:
        print(f"Section {section} not found. Using default value {default}")
        return default

def from_config_formula(section: str = None) -> dict:
    '''
    Returns dictionary from config.yaml file
    
    section: str = None
    '''
    default = {"p": 1, "q": 1, "zeta": 1, "effort": 1, "alpha": 1, "beta": 1, "c": 1} #  default formula

    with open("config.yaml", 'r') as file:
        config = yaml.safe_load(file)
    if section is None:
        return default
    try:
        return config[section]
    except KeyError:
        print(f"Section {section} not found. Using default value {default}")
        return default

def calculate_time_budget(time: int, config_formula: dict = None) -> int:
    '''
    Calculate time or daily budget: \n
    $$time * c$$
    
    shift_duration: int \n
    config_formula: dict {}
    '''
    if time == np.iinfo(np.int64).max:
        return np.iinfo(np.int64).max
    return int(round(time * config_formula["c"]))

def calculate_demand(population: int, config_formula: dict = None) -> int:
    '''
    Calculate demand in location i to satisfy: \n
    $$q_{i} * \\zeta_{i} * effort_{i}^\\alpha * residents_i^\\beta$$ \n
    If calculated demand more than population multiplied by \\zeta -> demand = population \n
    Demand can not be less than 1
    
    population: int \n
    config_formula: dict {}
    '''
    if config_formula is None:
        config_formula = {"p": 1, "q": 1, "zeta": 1, "effort": 1, "alpha": 1, "beta": 1, "c": 1}
    
    demand = (config_formula["q"] * 
        config_formula["zeta"] *
        pow(
            config_formula["effort"] * population,
            config_formula["alpha"]
        ) *
        pow(
            population, 
            config_formula["beta"]
        ))
    
    if demand > population * config_formula["zeta"]:
        demand = population * config_formula["zeta"] # set maximum number of eligible population per location
    elif demand < 1:
        demand = 1 # set minimum demand per location
    demand = round(demand)
    return int(demand)

def calculate_service_duration(demand: int, edge_weight_to_depot: int, shift_duration: int, config_formula: dict = None) -> int:
    '''
    Calculate service duration in location i: \n
    $$demand * effort$$ \n
    Service duration can not be more than duration shift excluding time for traversing distance from depot to location and back
    Service duration can not be less than 1
    
    demand: int \n
    edge_weight_to_depot: int \n
    shift_duration: int \n
    config_formula: dict {}
    '''
    if config_formula is None:
        config_formula = {"p": 1, "q": 1, "zeta": 1, "effort": 1, "alpha": 1, "beta": 1, "c": 1}
    service_duration = demand * config_formula["effort"]

    if service_duration > (shift_duration - edge_weight_to_depot):
        service_duration = shift_duration - edge_weight_to_depot
    elif service_duration < 1:
        service_duration = 1
    round(service_duration)
    return int(service_duration)

def calculate_prize(demand: int, config_formula: dict) -> int:
    '''
    Calculate prize for visiting location i: \n
    $$demand * p$$ \n
    Prize can not be less than 1
    
    demand: int \n
    config_formula: dict {}
    '''
    prize = demand * config_formula["p"]
    if prize < 1:
        prize = 1
    return int(round(prize))