# Language: Python 3
#
# Authors: Robert Costales
# Assignment: K-means / K-medians methods
# Date: 3/10/2017
#
# This program can use both the k-means and the k-medians method
# to group points into clusters.


from sklearn import datasets
import matplotlib.pyplot as plt
import random
import numpy as np
import turtle
from tkinter import *

# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_ RUN PREF _-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_- #

show_plot_init = False  # to show initial data plot
print_x_and_y = False   # print all x's and y's
show_final_plot = True  # show final plot
show_convergence = True     # show the updated values for m and b
print_centers = True        # prints the update of centers

num_clusters = 3     # number of clusters
max_iter = 10      # maximum iterations

# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_ TEXT BOX _-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_- #

k_means = False
k_medians = False
master = Tk()
master.title("MODE")
master.geometry("200x100")
t = Label(master, text="Type  '0'  for  k-means  method,\n '1'  for  k-medians  (default)")
t.pack()
e = Entry(master, width=20)
e.delete(0)
e.insert(0, "enter text here")
e.pack()
mode = 3
def callback():
    global mode
    mode = e.get()
    master.destroy()
b = Button(master, text="submit", width=20, command=callback)
b.pack()
master.mainloop()

if int(mode) == 0:
    k_means = True
else:
    k_medians = True


# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_ FUNCTIONS _-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_- #


def euclidean(p1, p2):
    """
    :param p1: first point in tuple (2D)
    :param p2: second point in tuple (2D)
    :return: euclidean distance between two points
    """
    d = (((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))**2
    return d


def manhattan(p1, p2):
    """
    :param p1: first point in tuple (2D)
    :param p2: second point in tuple (2D)
    :return: manhattan distance between two points
    """
    d = abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])
    return d


# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_ DATA _-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_- #

iris = datasets.load_iris()


x = []
for i in iris.data:     # creates x data
    x.append(i[0])
y = []
for i in iris.data:     # creates y data
    y.append(i[2])


if print_x_and_y:
    print("{0:>4} | {1:>2}\n--------------".format("X", "Y"))   # prints x and y values
    for i in range(len(x)):
        print("{0:>4.1f} | {1:4.1f}".format(x[i], y[i]))

if show_plot_init:              # shows initial plot of x and y
    plt.plot(x, y, "o")
    plt.show()

# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_ K-M METHODS _-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_- #

points = []
for i in range(len(x)):
    points.append([x[i], y[i], -1])         # creates list of all points

centers = []
for i in range(num_clusters):
    a = random.randint(0, len(points) - 1)     # randomize centers
    centers.append(points[a][0:2])

if print_centers:
    print(centers)


if k_means:
    print("k-means")
    for i in range(max_iter):
        # classify each point into a cluster (0 to num_clusters-1)
        for j in range(len(points)):  # j for each point
            shortest_distance = -1
            for k in range(num_clusters):  # k for each center
                current_distance = euclidean(centers[k], points[j])
                if current_distance < shortest_distance or shortest_distance == -1:
                    shortest_distance = current_distance
                    points[j][2] = k

        # find new ideal center for each cluster
        for k in range(num_clusters):
            x_count = 0
            y_count = 0
            count = 0
            for j in range(len(points)):
                if points[j][2] == k:
                    x_count += points[j][0]
                    y_count += points[j][1]
                    count += 1
            new_center = [x_count/count, y_count/count]
            centers[k] = new_center

        if print_centers:
            print(centers)


if k_medians:
    print("k-medians")
    for i in range(max_iter):

        # classify each point into a cluster (0 to num_clusters-1)
        for j in range(len(points)):  # j for each point
            shortest_distance = -1
            for k in range(num_clusters):  # k for each center
                current_distance = manhattan(centers[k], points[j])
                if current_distance < shortest_distance or shortest_distance == -1:
                    shortest_distance = current_distance
                    points[j][2] = k

        # find new ideal center for each cluster
        for k in range(num_clusters):
            x_temp = []
            y_temp = []
            count = 0
            for j in range(len(points)):
                if points[j][2] == k:
                    x_temp.append(points[j][0])
                    y_temp.append(points[j][1])
                    count += 1
            new_center = [np.median(x_temp), np.median(y_temp)]
            centers[k] = new_center

        if print_centers:
            print(centers)


# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_ FINAL PLOTS _-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_- #


colors = ["b", "g", "r", "c", "m", "y"]
black = "k"
for i in range(len(points)):
    color = colors[(points[i][2]) % len(colors)]
    plt.scatter(x=points[i][0], y=points[i][1], color=color)


for i in range(len(centers)):
    plt.scatter(x=centers[i][0], y=centers[i][1], color=black)

plt.show()
