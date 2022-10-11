from dataclasses import dataclass

@dataclass
class Anomaly:
    '''
    Initalize an anomaly.
    An anomaly takes the following parameters:
    - x_pos         x-coordinate of anomaly
    - dim           [x,y,z] dimensions of the anomaly
    - drho          Difference in density
    - depth         Depth of the anomaly
    '''
    x_pos: float
    dim: list
    drho: float
    depth: float