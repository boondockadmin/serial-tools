import matplotlib.animation as animation

class Plotting:
    def __init__(self, ax):
        self.ax = ax
        self.x_data = []
        self.y_data = []
        self.plotting = False

    def start_plotting(self):
        self.plotting = True
        self.ax.clear()
        self.ax.set_xlabel('X-axis')
        self.ax.set_ylabel('Y-axis')
        self.ani = animation.FuncAnimation(self.fig, self.update_plot, interval=1000)

    def update_plot(self, frame):
        if self.plotting and len(self.x_data) > 0:
            self.ax.clear()
            self.ax.plot(self.x_data, self.y_data)
            self.canvas.draw()

    def add_data(self, x, y):
        self.x_data.append(x)
        self.y_data.append(y)
