import numpy as np

def gravprism(drho,dx1,dx2,dy1,dy2,dz1,dz2):
    '''
    gravitational attraction due to "m" prisms at "n" observation point
    x1,x2,y1,y2,z1,z2 are coordinates of edges of prisms relative to 
    observation points  They are m x n matrices
    PS. Do not ever get me to do this again.....
    '''

    gam=(6.6732*10**(-11))*1e5             # mGal m^2/kg    
    num_points = len(dx1)
    
    d111 = np.column_stack((dx1, [dy1,]*num_points, [dz1,]*num_points))
    d112 = np.column_stack((dx2, [dy1,]*num_points, [dz1,]*num_points))
    d121 = np.column_stack((dx1, [dy2,]*num_points, [dz1,]*num_points))
    d122 = np.column_stack((dx2, [dy2,]*num_points, [dz1,]*num_points))
    d211 = np.column_stack((dx1, [dy1,]*num_points, [dz2,]*num_points))
    d212 = np.column_stack((dx2, [dy1,]*num_points, [dz2,]*num_points))
    d221 = np.column_stack((dx1, [dy2,]*num_points, [dz2,]*num_points))
    d222 = np.column_stack((dx2, [dy2,]*num_points, [dz2,]*num_points))

    R111 = np.linalg.norm(d111,axis=1)
    R112 = np.linalg.norm(d112,axis=1)
    R121 = np.linalg.norm(d121,axis=1)
    R122 = np.linalg.norm(d122,axis=1)
    R211 = np.linalg.norm(d211,axis=1)
    R212 = np.linalg.norm(d212,axis=1)
    R221 = np.linalg.norm(d221,axis=1)
    R222 = np.linalg.norm(d222,axis=1)

    g111=np.multiply(-1, np.subtract(np.subtract(np.multiply(dz1, np.arctan(np.divide(np.multiply(dx1, dy1), np.multiply(dz1, R111)))), np.multiply(dx1, np.log(np.add(R111, dy1)))), np.multiply(dy1, np.log(np.add(R111, dx1)))))
    g112=np.subtract(np.subtract(np.multiply(dz1, np.arctan(np.divide(np.multiply(dx2, dy1), np.multiply(dz1, R112)))), np.multiply(dx2, np.log(np.add(R112, dy1)))), np.multiply(dy1, np.log(np.add(R112, dx2))))
    g121=np.subtract(np.subtract(np.multiply(dz1, np.arctan(np.divide(np.multiply(dx1, dy2), np.multiply(dz1, R121)))), np.multiply(dx1, np.log(np.add(R121, dy2)))), np.multiply(dy2, np.log(np.add(R121, dx1))))
    g122=np.multiply(-1, np.subtract(np.subtract(np.multiply(dz1, np.arctan(np.divide(np.multiply(dx2, dy2), np.multiply(dz1, R122)))), np.multiply(dx2, np.log(np.add(R122, dy2)))), np.multiply(dy2, np.log(np.add(R122, dx2)))))

    g211=np.subtract(np.subtract(np.multiply(dz2, np.arctan(np.divide(np.multiply(dx1, dy1), np.multiply(dz2, R211)))), np.multiply(dx1, np.log(np.add(R211, dy1)))), np.multiply(dy1, np.log(np.add(R211, dx1))))
    g212=np.multiply(-1, np.subtract(np.subtract(np.multiply(dz2, np.arctan(np.divide(np.multiply(dx2, dy1), np.multiply(dz2, R212)))), np.multiply(dx2, np.log(np.add(R212, dy1)))), np.multiply(dy1, np.log(np.add(R212, dx2)))))
    g221=np.multiply(-1, np.subtract(np.subtract(np.multiply(dz2, np.arctan(np.divide(np.multiply(dx1, dy2), np.multiply(dz2, R221)))), np.multiply(dx1, np.log(np.add(R221, dy2)))), np.multiply(dy2, np.log(np.add(R221, dx1)))))
    g222=np.subtract(np.subtract(np.multiply(dz2, np.arctan(np.divide(np.multiply(dx2, dy2), np.multiply(dz2, R222)))), np.multiply(dx2, np.log(np.add(R222, dy2)))), np.multiply(dy2, np.log(np.add(R222, dx2))))

    dg = np.multiply(drho*gam,np.sum([g111,g112,g121,g122,g211,g212,g221,g222],0))

    return dg
