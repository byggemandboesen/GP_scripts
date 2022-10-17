import numpy as np
from dataclasses import dataclass
from modules.grav_anomaly.gravprism import gravprism

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

    def computeAnomaly(self, x_coords):
        dx1 = np.subtract(np.subtract(x_coords,self.dim[0]/2),self.x_pos)
        dx2 = np.subtract(np.add(x_coords,self.dim[0]/2),self.x_pos)
        dy1 = -self.dim[1]/2
        dy2 = self.dim[1]/2
        dz1 = self.depth
        dz2 = self.depth+self.dim[2]
        
        return gravprism(self.drho, dx1,dx2, dy1, dy2, dz1, dz2)