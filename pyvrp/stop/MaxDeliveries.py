from pyvrp._pyvrp import Client
from pyvrp.preprocess_data import from_config_float

class MaxDeliveries:
    """
    Criterion that stops after a maximum number of deliveries.
    """

    def __init__(self, clients: list[Client]):
        max_deliveries: int = 0
        for client in clients:
            max_deliveries += sum(client.delivery)

        self._max_deliveries = max_deliveries * from_config_float(section = "stop_fun", default = 1)
        self._curr_deliveries = 0

    def __call__(self, clients: list[Client]) -> bool:
        for client in clients:
            self._curr_deliveries += sum(client.delivery)

        return self._curr_deliveries >= self._max_deliveries