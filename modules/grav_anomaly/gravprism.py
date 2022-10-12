import numpy as np

def gravprism(drho,dx1,dx2,dy1,dy2,dz1,dz2):
    #
    # gravitational attraction due to "m" prisms at "n" observation point
    # x1,x2,y1,y2,z1,z2 are coordinates of edges of prisms relative to 
    # observation points  They are m x n matrices
    #---------------------------------------------------------------------

    gam=(66732*10**(-11))*1e5             # mGal m^2/kg
    
    num_points = len(dx1)
    print(dx1[0])
    d111 = np.column_stack((dx1, [dy1,]*num_points, [dz1,]*num_points))
    d112 = np.column_stack((dx1, [dy1,]*num_points, [dz2,]*num_points))
    d121 = np.column_stack((dx1, [dy2,]*num_points, [dz1,]*num_points))
    d122 = np.column_stack((dx1, [dy2,]*num_points, [dz2,]*num_points))
    d211 = np.column_stack((dx2, [dy1,]*num_points, [dz1,]*num_points))
    d212 = np.column_stack((dx2, [dy1,]*num_points, [dz2,]*num_points))
    d221 = np.column_stack((dx2, [dy2,]*num_points, [dz1,]*num_points))
    d222 = np.column_stack((dx2, [dy2,]*num_points, [dz2,]*num_points))

    R111 = np.linalg.norm(d111,axis=1)
    R112 = np.linalg.norm(d112,axis=1)
    R121 = np.linalg.norm(d121,axis=1)
    R122 = np.linalg.norm(d122,axis=1)
    R211 = np.linalg.norm(d211,axis=1)
    R212 = np.linalg.norm(d212,axis=1)
    R221 = np.linalg.norm(d221,axis=1)
    R222 = np.linalg.norm(d222,axis=1)
    print(R111[0])

    g111=np.multiply(-1,[dz1*np.arctan((dx1*dy1)/(dz1*R111))-dx1*np.log(R111+dy1)-dy1*np.log(R111+dx1)])
    g112=[np.multiply(dz1,np.arctan((dx2*dy1)/(dz1*R112)))-dx2*np.log(R112+dy1)-dy1*np.log(R112+dx2)]
    g121=[np.multiply(dz1,np.arctan((dx1*dy2)/(dz1*R121)))-dx1*np.log(R121+dy2)-dy2*np.log(R121+dx1)]
    g122=np.multiply(-1,[dz1*np.arctan((dx2*dy2)/(dz1*R122))-dx2*np.log(R122+dy2)-dy2*np.log(R122+dx2)])

    g211=[dz2*np.arctan((dx1*dy1)/(dz2*R211))-dx1*np.log(R211+dy1)-dy1*np.log(R211+dx1)]
    g212=np.multiply(-1,[dz2*np.arctan((dx2*dy1)/(dz2*R212))-dx2*np.log(R212+dy1)-dy1*np.log(R212+dx2)])
    g221=np.multiply(-1,[dz2*np.arctan((dx1*dy2)/(dz2*R221))-dx1*np.log(R221+dy2)-dy2*np.log(R221+dx1)])
    g222=[dz2*np.arctan((dx2*dy2)/(dz2*R222))-dx2*np.log(R222+dy2)-dy2*np.log(R222+dx2)]

    return np.multiply(drho*gam,np.sum([g111,g112,g121,g122,g211,g212,g221,g222],0))
