from plotter import Plotter

# Import Points for Classification
def import_data(path):
    raw_list = []
    data_list = []
    with open(path, "r") as f:
        for line in f.readlines():
            raw_list.append(line.split(','))

    raw_list = raw_list[1:] # getting rid of the headings

    for i in range(len(raw_list)): # converting coordinates to float
        data_list.append([float(raw_list[i][1]), float(raw_list[i][2])])

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

# Adapted from https://www.kite.com/python/answers/how-to-determine-if-a-point-is-on-a-line-segment-in-python
def on_line_seg(x1, y1, x2, y2, input_x, input_y): # using poin/slope formula to determine if input point is on line segment of polygon
    if x1 != x2:
        slope = (y2 - y1)/(x2 - x1)
        on_line = input_y - y1 == slope * (input_x - x1)
        line_seg_mbr = (minimum(x1,x2) <= input_x <= maximum(x1,x2)) and (minimum(y1,y2) <= input_y <= maximum(y1,y2)) # using mbr method to confirm point is in between points of line segments
        on_border = on_line and line_seg_mbr
        if on_border == True:
            return 'Boundary'
        else:
            return 'Unclassified'
    else:
        on_border = (x2 == input_x) and (minimum(y1,y2) <= input_y <= maximum(y1,y2))
        if on_border == True:
            return 'Boundary'
        else:
            return 'Unclassified'


# Polygon Class and creating MBR
class Poly:

    def __init__(self, poly_points):
        self.poly_points = poly_points
        self.values_list()
        self.lines_list()

    def values_list(self):
        self.x_values = []
        self.y_values = []
        for i in range(len(self.poly_points)):
            self.x_values.append(self.poly_points[i][0])
            self.y_values.append(self.poly_points[i][1])
        print(self.x_values)
        print(self.y_values)

    def lines_list(self):
        self.lines = []
        p1 = self.x_values[0], self.y_values[0]
        for i in range(len(self.poly_points)):
            if i == 0:
                continue
            else:
                self.lines.append(tuple([p1,(self.x_values[i],self.y_values[i])]))
                p1 = self.x_values[i], self.y_values[i]
        self.lines.append(tuple([p1,(self.x_values[0],self.y_values[0])]))
        print(self.lines)

    def on_line(self, input_points):
        res = []
        for item in input_points:
            if item in self.poly_points:
                res.append('Boundary')
            else:
                for line in self.lines:
                    # if line[0][0] == line[1][0]:
                    #     res.append('Boundary')
                    # if (item[0] - line[0][0])/(line[1][0] - line[0][0]) = (item[1] - line[0][1])/(line[1][1] - line[0][1]):
                    #     res.append()
                    # print(line)
                    pass
                res.append('Unclassified')
        self.results = res




        #  x* - x1/x2 - x1 = y* - y1 / y2 - y1 if this equality holds then the point x*,y* is on the line
        # if x2 = x1 it results in not defined so x* is on the line if x* = x2 or x* = x1

   # def rca(self):

        # loop through points objects and establish corresponding ray points (very large x values)
        # write formula for intersection



    def mbr(self):
        self.min_x = minimum(self.x_values)
        self.min_y = minimum(self.y_values)
        self.max_x = maximum(self.x_values)
        self.max_y = maximum(self.y_values)
        # print('MBR:')
        # print('Lower Left:', '(',self.min_x, self.min_y,')')
        # print('Upper Left:', '(',self.min_x, self.max_y, ')')
        # print('Upper Right:', '(',self.max_x, self.max_y, ')')
        # print('Lower Right:', '(', self.max_x, self.min_y, ')')

    def classify_mbr(self, x, y):
        if (x <= self.max_x) and (y <= self.max_y) and (x >= self.min_x) and (y >= self.min_y):
            return 'inside'
        else:
            return 'outside'


# Creating input point class
class Point:
    def __init__(self, points):
        self.points = points

    def get_point(self, i):
        return self.points[i][1],self.points[i][2]

    # def get_all_points(self):
    #     points_list = []
    #     for i in range(len(self.points)):  # converting coordinates to float
    #         points_list.append([float(self.points[i][1]), float(self.points[i][2])])
    #     return points_list

    # def get_id(self):
    #     return self.id
    # def get_x(self):
    #     return self.x
    #
    # def get_y(self):
    #     return self.y
def main():
    poly = import_data("C:/Users/17075/Assignment_1/Project Template/polygon.csv")
    print(poly)
    points = import_data("C:/Users/17075/Assignment_1/Project Template/input.csv")
    print(points)
    test = Poly(poly)
    # test.mbr()

    point_test = Point(points)
    test.on_line(point_test.points)

    # point_test.get_point(0)
    # x,y = point_test.get_point(0)
    # print('({},{})'.format(x,y))
    #print(f'({x},{y})')
    #print(test.classify_mbr(x,y))

    # plot = Plotter()
    # plot.add_polygon(test.x_values,test.y_values)
    # plot.add_point(x,y,kind='inside')
    # plot.show()


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