import matplotlib.pyplot as plt

def main():

    flag = True

    for i in range (5):

        plot_obstacles()
        plot_points()
        
        if flag:
            plt.plot([3, 5], [2, 6], '-')
        else:
            plt.plot([3, 6], [2, 7], '-')

        plt.pause(0.5)

        flag = not flag

    plt.show()
    

def plot_points():
    node_x = []
    node_y = []

    for element in [(3,2),(6,7),(15,8),(5,6)]:
        node_x.append(element[0])
        node_y.append(element[1])

    plt.plot(node_x, node_y, "ko")

def plot_obstacles():

    plt.clf()
    plt.axis([0, 20, 1, 40])
    obs_1_x = [2.5, 3.5, 3.5, 2.5, 2.5]
    obs_1_y = [9, 9, 12, 12, 9]
    plt.fill(obs_1_x, obs_1_y, "b")

if __name__ == '__main__':
    
    main()