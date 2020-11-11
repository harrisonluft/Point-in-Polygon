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

def export_data(path, exports):
    id = []
    n = 1
    for i in range(len(exports)):
        id.append(str(n+i))
    with open(path, "w") as f:
        f.write(','.join(['ID','classifications','\n']))
        for j in range(len(exports)):
            f.write(','.join([id[j], exports[j],'\n']))


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
def get_intersect(x1, y1, x2, y2, x3, y3, x4, y4): # only identifies non coincident intersections, returns None for coincident lines
# returns a (x, y) tuple or None if there is no intersection
# will use the (x, y) return as a reference to the original lines to adjust for crossing vertices
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


def intersect_check(x1, y1, x2, y2, x3, y3, x4, y4):
    # if mbr intersect, check collinearity as a marker for checking vertices
    if overlap_check(x1, y1, x2, y2, x3, y3, x4, y4):
        return 'Collinear'
    else:
        return get_intersect(x1, y1, x2, y2, x3, y3, x4, y4)

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


    def mbr(self):
        self.min_x = minimum(self.x_values)
        self.min_y = minimum(self.y_values)
        self.max_x = maximum(self.x_values)
        self.max_y = maximum(self.y_values)


    def classify_mbr(self, x, y):
        if (x <= self.max_x) and (y <= self.max_y) and (x >= self.min_x) and (y >= self.min_y):
            return 'Inside'
        else:
            return 'Outside'


    def rca(self, ray_lines):
        res = []
        for item in ray_lines: # for each input point  run the following
            temp = []
            if self.classify_mbr(item[0][0], item[0][1]) == 'Outside': # determine inside/outside for MBR
                temp.append('Outside')
            elif item in self.poly_points: # Assign boundary points if in polygon boundary points
                temp.append('Boundary')
            else:
                for line in self.lines:
                    if on_line_seg(line[0][0], line[0][1], line[1][0], line[1][1], item[0][0], item[0][1]):
                        temp.append('Boundary')
                    else:
                        temp.append(intersect_check(line[0][0], line[0][1], line[1][0], line[1][1], item[0][0], item[0][1], item[1][0], item[1][1]))
            res.append(temp)
        self.results = res


    def count(self):
        counter = []
        for item in self.results:
            n = 0  # need to deal with boundary points out of loop
            for i in range(len(item)):
                if i == (len(item)-2):  # need to specify case for end of list -2 since there are '+2' cases
                    if item[i] == 'Outside':
                        n = 0
                    elif item[i] == None:  # if no intersection do not add to count
                           pass
                    elif item[i+1] == 'Collinear': # if intersects collinear line then do same test as vertex above
                        self.max_y1  = max(self.lines[i][1][1], self.lines[i][0][1])  # orientation for line 1
                        self.max_y2 = max(self.lines[1][1][1], self.lines[1][0][1])  # orientation for line +2
                        if (self.max_y1  > item[i][1] and self.max_y2 > item[0][1]) or (self.max_y1  < item[i][1] and self.max_y2 < item[0][1]): # if they are the same record 0 count
                            pass
                        else: # if not, record +1
                            n += 1
                    elif item[i] == item[i+1] and item[i] != 'Boundary':  # vertex intersection
                        self.max_y1  = max(self.lines[i][1][1], self.lines[i][0][1])  # orientation for line 1
                        self.max_y2 = max(self.lines[0][1][1], self.lines[0][0][1])  # orientation for line +2
                        if (self.max_y1  > item[i][1] and self.max_y2 > item[i+1][1]) or \
                                (self.max_y1 == item[i][1] and self.max_y2 == item[i+1][1]):  # test orientation
                            pass
                        else:  # record +1 of opposing lines
                            n += 1
                    elif (item[i] == item[i-1]) or item[i] == 'Collinear' or item[i-1] == 'Collinear':
                        pass
                    else:
                        n += 1
                elif i == (len(item)-1): # specify cases for end of list since there are +1/+2 cases
                    if item[i] == 'Outside':
                        n = 0
                    elif item[i] == None: # if no intersection do not add to count
                            n = n
                    elif item[0] == 'Collinear': # if intersects collinear line then do same test as vertex above
                        self.max_y1  = max(self.lines[i][1][1], self.lines[i][0][1])  # orientation for line 1
                        self.max_y2 = max(self.lines[1][1][1], self.lines[1][0][1])  # orientation for line 2
                        if (self.max_y1 > item[i][1] and self.max_y2 > item[1][1]) or \
                                (self.max_y1 < item[i][1] and self.max_y2 < item[1][1]): # if they are the same record 0 count
                            n = n
                        else:  # record +1 of opposing lines
                            n += 1
                    elif item[i] == item[0] and item[i] != 'Boundary': # if intersections are the same for two sequential lines
                        self.max_y1  = max(self.lines[i][1][1], self.lines[i][0][1]) # see what the orientation is for line 1
                        self.max_y2 = max(self.lines[0][1][1], self.lines[0][0][1]) # see what the orientation is for line 2
                        if (self.max_y1  > item[i][1] and self.max_y2 > item[0][1]) or (self.max_y1 == item[i][1] and self.max_y2 == item[0][1]): # if they are the same do not count
                            n = n
                        else: # if not, record +1
                            n += 1
                    elif (item[i] == item[i-1]) or item[i] == 'Collinear' or item[i-1] == 'Collinear':
                        pass
                    else:
                        n += 1
                else:
                    if item[i] == 'Outside':
                        n = 0
                    elif item[i] == None: # if no intersection do not add to count
                            pass
                    elif item[i+1] == 'Collinear': # if intersects collinear line then do same test as vertex above
                        self.max_y1 = max(self.lines[i][1][1], self.lines[i][0][1])  # see what the orientation is for line 1
                        self.max_y2 = max(self.lines[i + 2][1][1], self.lines[i + 2][0][1])  # see what the orientation is for line 2
                        if (self.max_y1 > item[i][1] and self.max_y2 > item[i+2][1]) or (self.max_y1 < item[i][1] and self.max_y2 < item[i+2][1]): # if they are the same record 0 count
                            pass
                        else: # if not, record +1
                            n += 1
                    elif item[i] == item[i+1] and item[i] != 'Boundary': # if intersections are the same for two sequential lines
                        self.max_y1 = max(self.lines[i][1][1], self.lines[i][0][1]) # see what the orientation is for line 1
                        self.max_y2 = max(self.lines[i+1][1][1], self.lines[i+1][0][1]) # see what the orientation is for line 2
                        if (((self.max_y1 > item[i][1]) and (self.max_y2 > item[i+1][1])) or ((self.max_y1 == item[i][1]) and (self.max_y2 == item[i+1][1]))): # if they are the same do not count
                            pass
                        else: # if not, record +1
                            n += 1
                    elif (item[i] == item[i-1]) or item[i] == 'Collinear' or item[i-1] == 'Collinear':
                        pass
                    else:
                        n += 1
            for i in range(len(item)):
                if item[i] == 'Boundary':
                    n = -1
                else:
                    pass
            counter.append(n)
        self.count = counter

    def define_label(self):
        label = []
        for n in self.count:
            if (n % 2) == 0:
                label.append('outside')
            elif n < 0:
                label.append('boundary')
            elif (n % 2) != 0:
                label.append('inside')
        self.point_label = label
        print(self.point_label)


# Creating input point class
class Point:
    def __init__(self, points):
        self.points = points

    def get_point(self, i):
        return self.points[i][0], self.points[i][1]

    def ray_lines(self, mbr_max_x):
        self.rca_x = mbr_max_x + 1
        self.ray_lines = []
        for i in range(len(self.points)):
            self.ray_lines.append(tuple([(self.points[i][0], self.points[i][1]), (self.rca_x, self.points[i][1])]))
        return self.ray_lines


def main(polygon_path, input_points_path, output_path):
    plot = Plotter()

    # import data
    poly_points = import_data(polygon_path)
    points = import_data(input_points_path)

    # init Polygon class
    polygon = Poly(poly_points)

    # create bounding box for polygon
    polygon.mbr()

    # init Point class
    input_points = Point(points)

    # create ray's for each point based on max x value of polygon bounding box
    input_points.ray_lines(polygon.max_x)

    # generate list with intersections, collinear instances, boundaries and MBR tests
    polygon.rca(input_points.ray_lines)

    # count based on elements in list: +1 for plain intersection,
    # +0 for same side vertex/coincident instance,
    # and +1 for dual side vertex/coincident instance
    # borders are given as -1,
    # outside mbr is given 0
    polygon.count()

    # apply labels to counts
    polygon.define_label()
    export_data(output_path, polygon.point_label)
    # plot
    plot.add_polygon(polygon.x_values, polygon.y_values)
    for i in range(len(input_points.points)):
        plot.add_point(input_points.points[i][0], input_points.points[i][1], kind=polygon.point_label[i])
    plot.show()


if __name__ == '__main__':
    main("C:/Users/17075/Assignment_1/Project Template/polygon.csv",
         "C:/Users/17075/Assignment_1/Project Template/input.csv",
         "C:/Users/17075/Assignment_1/Project Template/output_test.csv")
