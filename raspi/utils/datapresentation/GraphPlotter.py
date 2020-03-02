import matplotlib.pyplot as plt
import numpy

plt.style.use("ggplot")


class GraphPlotter:
    def __init__(self, pauseTime: float = 0.01, yRange=[0, 0.5]):
        # TODO: Init stuff
        plt.ion()
        self.pause_time = pauseTime
        self.figure_list = []
        self.y_range = yRange

    def add_plot(self, identifier: str, title: str = ""):

        x_vec = numpy.linspace(0, 1, 101)[0:-1]
        y_vec = [0] * len(x_vec)
        if title == "":
            title = identifier

        (line_value,) = plt.plot(x_vec, y_vec, "-o", alpha=0.8, label=title)
        plt.legend()
        self.figure_list.insert(
            len(self.figure_list),
            {"identifier": identifier, "line_value": line_value, "y_vec": y_vec},
        )

    def show_graph(self):
        plt.show()

    def input_value(self, idenifier: str, value: float):
        # Input value based on identifier
        modify_object = {}
        for graph_item in self.figure_list:
            if graph_item["identifier"] == idenifier:
                modify_object = graph_item

        if modify_object == {}:
            return

        modify_object["y_vec"][-1] = value
        modify_object["line_value"].set_ydata(modify_object["y_vec"])
        plt.ylim(self.y_range)
        modify_object["y_vec"] = numpy.append(modify_object["y_vec"][1:], 0.0)
        plt.pause(self.pause_time)
