import numpy as np
import matplotlib.pyplot as plt
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import math
import time

def lorenz(x, y, z, s=10, r=28, b=float(8/3)):
    '''
    Given:
       x, y, z: a point of interest in three dimensional space
       s, r, b: parameters defining the lorenz attractor
    Returns:
       x_dot, y_dot, z_dot: values of the lorenz attractor's partial
           derivatives at the point x, y, z
    '''
    x_dot = s*(y - x)
    y_dot = r*x - y - x*z
    z_dot = x*y - b*z
    return x_dot, y_dot, z_dot


def chenz(x, y, z, a=35, b=3, c=28):
    x_dot = a*(y - x)
    y_dot = (c-a)*x - x*z + c*y
    z_dot = x*y - b*z
    return x_dot, y_dot, z_dot


def convert_int(float_number, limit, significative):
    int_number = (math.floor(float_number * 10 ** significative) % limit) #+ 1
    return int_number


def iterator_random_position(system, dt, initial_conditions, max):
    i = 0 
    xs = []
    ys = []
    zs = []
    test = []
    test1 = []
    test2 = []

    xs.append(initial_conditions[0])
    ys.append(initial_conditions[1])
    zs.append(initial_conditions[2])
    
    while True:
        if len(test) == max and len(test1) == max and len(test2) == max :
            break;
        
        x_dot, y_dot, z_dot = system(xs[i], ys[i], zs[i])
        xs.append(xs[i] + (x_dot * dt))
        ys.append(ys[i] + (y_dot * dt))
        zs.append(zs[i] + (z_dot * dt))

        data = convert_int(xs[i+1], max, 14) 
        data1 = convert_int(ys[i+1], max, 14)
        data2 = convert_int(zs[i+1], max, 14)
        
        if data not in test:
            test.append(data)
        if data1 not in test1:
            test1.append(data1)
        if data2 not in test2:
            test2.append(data2)

        i = i + 1
    
    initial_conditions = [xs[len(xs)-1], ys[len(xs)-1], zs[len(xs)-1]]
  
    return test, test1, test2, initial_conditions

def iterator_random_cipher(system, dt, initial_conditions, max):
    xs = []
    ys = []
    zs = []
    test = []
    test1 = []
    test2 = []

    xs.append(initial_conditions[0])
    ys.append(initial_conditions[1])
    zs.append(initial_conditions[2])

    for i in range(max):
        x_dot, y_dot, z_dot = system(xs[i], ys[i], zs[i])
        xs.append(xs[i] + (x_dot * dt))
        ys.append(ys[i] + (y_dot * dt))
        zs.append(zs[i] + (z_dot * dt))

        test.append(convert_int(xs[i+1], max, 14))
        test1.append(convert_int(ys[i+1], max, 14))
        test2.append(convert_int(zs[i+1], max, 14))

    initial_conditions = [xs[len(xs)-1], ys[len(xs)-1], zs[len(xs)-1]]    

    return test, test1, test2, initial_conditions




# start = time.process_time()

# test, test1, test2, initial_conditions = iterator_random_cipher(chenz, 0.001,[0., 1., 1.05], 200000 )

# print(time.process_time() - start)



# Plot
# fig = plt.figure()
# ax = fig.gca(projection='3d')

# ax.plot(xs, ys, zs, lw=0.5)
# # ax.plot(test, test1, test2, lw=0.5)
# ax.set_xlabel("X Axis")
# ax.set_ylabel("Y Axis")
# ax.set_zlabel("Z Axis")
# ax.set_title("Lorenz Attractor")

# plt.show()

# plt.plot(test)
# plt.plot(test1)
# plt.plot(test2)
# plt.show()



# def nonlinear_iteration(system, dt, num_steps, initial_conditions):

#     # Need one more for the initial values
#     xs = np.empty(num_steps + 1)
#     ys = np.empty(num_steps + 1)
#     zs = np.empty(num_steps + 1)
#     xs[0], ys[0], zs[0] = initial_conditions[0], initial_conditions[1], initial_conditions[2]
    
#     for i in range(num_steps):
#         x_dot, y_dot, z_dot = system(xs[i], ys[i], zs[i])
#         xs[i + 1] = xs[i] + (x_dot * dt)
#         ys[i + 1] = ys[i] + (y_dot * dt)
#         zs[i + 1] = zs[i] + (z_dot * dt)
#     return xs, ys, zs

