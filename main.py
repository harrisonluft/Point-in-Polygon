from plotter import Plotter

# Import Points for Classification
def import_data(path):
    data_list = []
    with open(path, "r") as f:
        for line in f.readlines():
            data_list.append(line.split(','))

    data_list = data_list[1:] # getting rid of the headings

    for i in range(len(data_list)): # converting coordinates to float
            data_list[i][0] = float(data_list[i][0])
            data_list[i][1] = float(data_list[i][1])
            data_list[i][2] = float(data_list[i][2])
    return data_list

# Minimum and Maximum functions

def minimum(values):
    smallest = values[0]
    for i in values[1:]:
        if smallest > i:
            smallest = i
    return smallest


def maximum(values):
    biggest = values[0]
    for i in values[1:]:
        if biggest < i:
            biggest = i
    return biggest

# Polygon Class creating MBR
class Poly:

    def __init__(self, poly):
        self.poly = poly
        self.values_list()

    def values_list(self):
        self.x_values = []
        self.y_values = []
        for i in range(len(self.poly)):
            self.x_values.append(self.poly[i][1])
            self.y_values.append(self.poly[i][2])
        print(self.x_values)
        print(self.y_values)

    def mbr(self):
        self.min_x = minimum(self.x_values)
        self.min_y = minimum(self.y_values)
        self.max_x = maximum(self.x_values)
        self.max_y = maximum(self.y_values)
        print('MBR:')
        print('Lower Left:', '(',self.min_x, self.min_y,')')
        print('Upper Left:', '(',self.min_x, self.max_y, ')')
        print('Upper Right:', '(',self.max_x, self.max_y, ')')
        print('Lower Right:', '(', self.max_x, self.min_y, ')')

    def classify_mbr(self, x, y):
        if (x <= self.max_x) and (y <= self.max_y) and (x >= self.min_x) and (y >= self.min_y):
            return 'inside'
        else:
            return 'outside'


class Point:
    def __init__(self, points):
        self.points = points

    def get_point(self, i):
        return self.points[i][1],self.points[i][2]


    # def get_id(self):
    #     return self.id
    # def get_x(self):
    #     return self.x
    #
    # def get_y(self):
    #     return self.y
def main():
    poly = import_data("C:/Users/17075/Assignment_1/Project Template/polygon.csv")
    points = import_data("C:/Users/17075/Assignment_1/Project Template/input.csv")
    test = Poly(poly)
    test.mbr()

    point_test = Point(points)
    point_test.get_point(0)
    x,y = point_test.get_point(0)
    print('({},{})'.format(x,y))

    print(test.classify_mbr(x,y))

    plot = Plotter()
    plot.add_polygon(test.x_values,test.y_values)
    plot.add_point(x,y,kind='inside')
    plot.show()


if __name__ == '__main__':
    main()



# Want to store the min/max of the x's and y's in a class but don't know how to do this right now
# class Minimum_x_y:
#     def __init__(self, id, x, y):
#         super().__init__(id)
#         super().__init__(x)
#         super().__init__(y)

# Finding min/max using a function, first appending the min and max into their own lists
# This seems and inefficient way to do it, still thinking about it
# x_coords = []
# y_coords = []
# for i in range(len(poly)):
#     coords = Coordinates(poly[i][0], poly[i][1], poly[i][2])
#     x_coords.append(coords.get_x())
#     y_coords.append(coords.get_y())
#
# minimum_coords = (minimum(x_coords), minimum(y_coords))
# maximum_coords = (maximum(x_coords), maximum(y_coords))
#
# print(minimum_coords)
# print(maximum_coords)

# smallest = xs[0]
#         for coord_x in xs[1:]:
#             if smallest > coord_x:
#                 smallest = coord_x
#         return smallest

# coords = []
# for i in range(len(poly)):
#     coords.append([poly[i][1],poly[i][2]])