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
def on_line_seg(x1, y1, x2, y2, input_x, input_y): # using point/slope formula to determine if input point is on line segment of polygon
    if x1 != x2:
        slope = (y2 - y1)/(x2 - x1)
        on_line = input_y - y1 == slope * (input_x - x1)
        line_seg_mbr = (min(x1, x2) <= input_x <= max(x1, x2)) and (min(y1, y2) <= input_y <= max(y1, y2))
        # using mbr method to confirm point is in between points of line segments
        on_border = on_line and line_seg_mbr
        if on_border:
            return True
        else:
            return False
    else:
        on_border = (x2 == input_x) and (min(y1, y2) <= input_y <= max(y1, y2))
        if on_border:
            return True
        else:
            return False

# adapted from https://silentmatt.com/rectangle-intersection/
# Mbr's must intersect for lines to intersect.
# Because the ray's extend beyond the polygon's maximum bounds, if the boxes intersect
# there is an intersection.

# This does not take into account overlapping segments, will build another function for that.
# First check:
def mbr_seg(x1, y1, x2, y2, x3, y3, x4, y4):
    mbr_overlap = x1 <= x4 and x2 >= x3 and y1 <= y4 and y2 >= y3
    return mbr_overlap # True/False for intersection of bounding boxes

def overlap_check(x1, y1, x2, y2, x3, y3, x4, y4):
    y_overlap = y1 == y2 and y1 == y3 and y1 == y4
    x_overlap = x1 <= x4 and x2 >= x3
    overlap = y_overlap and x_overlap
    return overlap

# Adapted from https://rosettacode.org/wiki/Find_the_intersection_of_two_lines
def line_intersect(x1, y1, x2, y2, x3, y3, x4, y4): # only identifies non collinear intersections, returns None for collinear lines
# returns a (x, y) tuple or None if there is no intersection
# will use the (x, y) return to adjust for crossing vertices
    d = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
    if d:
        uA = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / d
        uB = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / d
    else:
        return
    if not (0 <= uA <= 1 and 0 <= uB <= 1):
        return
    x = x1 + uA * (x2 - x1)
    y = y1 + uA * (y2 - y1)
    return x, y


def rca(x1, y1, x2, y2, x3, y3, x4, y4):
    # if mbr intersect, check collinearity as a marker for checking vertices
    if overlap_check(x1, y1, x2, y2, x3, y3, x4, y4):
        return 'Collinear'
    else:
        return line_intersect(x1, y1, x2, y2, x3, y3, x4, y4)

    # if mbr_seg(x1, y1, x2, y2, x3, y3, x4, y4):



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
            return 'Inside'
        else:
            return 'Outside'


    def classify(self, ray_lines):
        res = []
        for item in ray_lines:
            temp = []
            if item in self.poly_points:
                temp.append('Boundary')
            elif self.classify_mbr(item[0][0], item[0][1]) == 'Outside':
                temp.append('Outside')
            else:
                for line in self.lines:
                    if on_line_seg(line[0][0], line[0][1], line[1][0], line[1][1], item[0][0], item[0][1]):
                        temp.append('Boundary')
                    else:
                        temp.append(rca(line[0][0], line[0][1], line[1][0], line[1][1], item[0][0], item[0][1], item[1][0], item[1][1]))

            res.append(temp)
        self.results = res
        print(self.results)
    # def classify_intersect(self):
    #     for

# Creating input point class
class Point:
    def __init__(self, points):
        self.points = points

    def get_point(self, i):
        return self.points[i][0],self.points[i][1]

    def ray_lines(self, mbr_max_x):
        self.rca_x = mbr_max_x + 1
        self.ray_lines = []
        for i in range(len(self.points)):
            self.ray_lines.append(tuple([(self.points[i][0], self.points[i][1]), (self.rca_x, self.points[i][1])]))
        return self.ray_lines



def main():
    poly = import_data("C:/Users/17075/Assignment_1/Project Template/polygon.csv")
    print(poly)
    points = import_data("C:/Users/17075/Assignment_1/Project Template/input.csv")
    print(points)
    test = Poly(poly) # init poly class, create x and y lists
    test.mbr() # create bounding box for polygon


    point_test = Point(points) # init point class
    #print(rca(3.0, 5.0, 2.0, 6.0, 1.0, 5.5, 5.0, 5.5))
    #print(rca(2.0, 6.0, 1.0, 5.0, 1.0, 5.5, 5.0, 5.5))
    # print(mbr_seg(2.0, 6.0, 1.0, 5.0, 1.0, 5.5, 5.0, 5.5))

    point_test.ray_lines(test.max_x) # create ray's for each point based on poly bounding box

    test.classify(point_test.ray_lines) # classify points

    # point_test.get_point(1)
    # x, y = point_test.get_point(1)
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