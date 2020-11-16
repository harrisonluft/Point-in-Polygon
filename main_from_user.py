from plotter import Plotter


def user_input():
    data_list = []
    while True:
        try:
            user_point = input('Please input coordinate as x, y: ')
            user_point_float = [float(user_point.split(',')[0]), float(user_point.split(',')[1])]
            break
        except:
            print('Invalid input, please try again')
    data_list.append(user_point_float)
    return data_list


def import_data(path):
    raw_list = []
    data_list = []
    with open(path, "r") as f:
        for line in f.readlines():
            raw_list.append(line.split(','))

    raw_list = raw_list[1:]  # getting rid of the headings

    for i in range(len(raw_list)):  # converting coordinates to float
        data_list.append([float(raw_list[i][1]), float(raw_list[i][2])])

    return data_list


def export_data(path, exports):
    id = []
    n = 1
    for i in range(len(exports)):
        id.append(str(n+i))
    with open(path, "w") as f:
        f.write(','.join(['ID', 'classifications', '\n']))
        for j in range(len(exports)):
            f.write(','.join([id[j], exports[j], '\n']))


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


# adapted from https://www.kite.com/python/answers/how-to-determine-if-a-point-is-on-a-line-segment-in-python
# using point/slope formula to determine if input point is on line segment of polygon
def on_line_seg(x1, y1, x2, y2, input_x, input_y):
    if x1 != x2:
        slope = (y2 - y1)/(x2 - x1)
        on_line = input_y - y1 == slope * (input_x - x1)
        line_seg_mbr = (min(x1, x2) <= input_x <= max(x1, x2)) and (min(y1, y2) <= input_y <= max(y1, y2))
        # using mbr methodology to confirm point is in between points of line segments
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


def overlap_check(x1, y1, x2, y2, x3, y3, x4, y4):  # identifies coincident lines
    y_overlap = y1 == y2 and y1 == y3 and y1 == y4
    x_overlap = x1 <= x4 and x2 >= x3
    overlap = y_overlap and x_overlap
    return overlap


# Adapted from https://rosettacode.org/wiki/Find_the_intersection_of_two_lines
# and Torben Jansen from https://observablehq.com/@toja/line-box-intersection published 1 Oct 2018
def get_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    # returns a (x, y) tuple or None if there is no intersection or coincident
    # will use the (x, y) return as a reference to the original lines to adjust for crossing vertices
    d = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
    if d:
        ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / d
        ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / d
    else:
        return
    if not (0 <= ua <= 1 and 0 <= ub <= 1):
        return
    x = x1 + ua * (x2 - x1)
    y = y1 + ua * (y2 - y1)
    return x, y


# outputs the kind of intersection for each point crossing each line in the polygon
def intersect_check(x1, y1, x2, y2, x3, y3, x4, y4):
    # if mbr intersect, check coincidence as a marker for checking vertices
    if overlap_check(x1, y1, x2, y2, x3, y3, x4, y4):
        return 'coincident'
    else:
        return get_intersect(x1, y1, x2, y2, x3, y3, x4, y4)


# function to translate list of intersection types into count of ray crossings.
def counter(line, line_plus_one, line_plus_two, point, point_plus_one, point_plus_two, point_minus_one, n_count):
    if point is None:  # if no intersection do not add to count
        pass
    elif point_plus_one == 'coincident':  # if intersects coincident then test orientations
        max_y1 = max(line[1][1], line[0][1])  # orientation for line before coincidence
        max_y2 = max(line_plus_two[1][1], line_plus_two[0][1])  # orientation for line after coincidence
        if (max_y1 > point[1] and max_y2 > point_plus_two[1]) or \
                (max_y1 == point[1] and max_y2 == point_plus_two[1]):  # if same orientation count 0
            pass
        else:  # if not, count +1
            n_count += 1
    elif point == point_plus_one and point != 'boundary':  # vertex identification
        max_y1 = max(line[1][1], line[0][1])  # orientation for line 1
        max_y2 = max(line_plus_one[1][1], line_plus_one[0][1])  # orientation for line i + 1
        if (max_y1 > point[1] and max_y2 > point_plus_one[1]) or \
                (max_y1 == point[1] and max_y2 == point_plus_one[1]):  # if same orientation count 0
            pass
        else:  # count +1 if opposing lines
            n_count += 1
    # ignore cases that would cause double counting
    elif (point == point_minus_one) or point == 'coincident' or point_minus_one == 'coincident':
        pass
    else:
        n_count += 1  # if ordinary intersection +1 to count
    return n_count


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
                self.lines.append(tuple([p1, (self.x_values[i], self.y_values[i])]))
                p1 = self.x_values[i], self.y_values[i]
        self.lines.append(tuple([p1, (self.x_values[0], self.y_values[0])]))

    # generate minimum bounding rectangle for first-pass inclusion/exclusion of input points
    def mbr(self):
        self.min_x = minimum(self.x_values)
        self.min_y = minimum(self.y_values)
        self.max_x = maximum(self.x_values)
        self.max_y = maximum(self.y_values)

    def classify_mbr(self, x, y):
        if (x <= self.max_x) and (y <= self.max_y) and (x >= self.min_x) and (y >= self.min_y):
            return 'inside'
        else:
            return 'outside'

    # generate list of mbr results, ray-line intersections, and coincidence for each point
    def rca_ray(self, ray_lines):
        res = []
        for item in ray_lines:
            temp = []
            if self.classify_mbr(item[0][0], item[0][1]) == 'outside':  # determine inside/outside for MBR
                temp.append('outside')
            elif item in self.poly_points:  # assign boundary points if in polygon boundary points
                temp.append('boundary')
            else:
                for line in self.lines:  # identify points residing on polygon borders
                    if on_line_seg(line[0][0], line[0][1], line[1][0], line[1][1],
                                   item[0][0], item[0][1]):
                        temp.append('boundary')
                    else:  # identify intersecting points and coincident lines
                        temp.append(intersect_check(line[0][0], line[0][1], line[1][0], line[1][1],
                                                    item[0][0], item[0][1], item[1][0], item[1][1]))
            res.append(temp)
        self.results = res

    # test orientation of intersections and coincidence and count line crossings
    def rca_count(self):
        count_list = []
        for item in self.results:
            n = 0
            for i in range(len(item)):
                # specify conditions for end of list since counter function references i + 1 and i + 2 points/lines
                if i == (len(item)-2):
                    n = counter(self.lines[i], self.lines[i + 1], self.lines[0],
                                item[i], item[i + 1], item[0], item[i - 1], n)

                elif i == (len(item)-1) and len(item) != 1:
                    n = counter(self.lines[i], self.lines[0], self.lines[1],
                                item[i], item[0], item[1], item[i - 1], n)
                elif i == 0:  # specify condition for first item in list since counter references i - 1
                    if item[i] == 'outside':
                        n = 0
                    else:
                        n = counter(self.lines[i], self.lines[i + 1], self.lines[i + 2],
                                    item[i], item[i + 1], item[i + 2], item[-1], n)
                else:  # general case for points not at end of list
                    n = counter(self.lines[i], self.lines[i + 1], self.lines[i + 2],
                                item[i], item[i + 1], item[i + 2], item[i - 1], n)
            for i in range(len(item)):
                if item[i] == 'boundary':
                    n = -1
                else:
                    pass
            count_list.append(n)
        self.count = count_list

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


# Creating input point class
class Points:
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


def main(polygon_path, output_path):
    plot = Plotter()

    # import data
    poly_points = import_data(polygon_path)
    points = user_input()

    # init Polygon class
    polygon = Poly(poly_points)

    # create bounding box for polygon
    polygon.mbr()

    # init Point class
    input_points = Points(points)

    # create ray's for each point based on max x value of polygon bounding box
    input_points.ray_lines(polygon.max_x)

    # generate list with intersections, collinear instances, boundaries and MBR tests
    polygon.rca_ray(input_points.ray_lines)

    # count based on elements in list: +1 for plain intersection,
    # +0 for same side vertex/coincident instance,
    # and +1 for dual side vertex/coincident instance
    # borders are given as -1,
    # outside mbr is given 0
    polygon.rca_count()

    # apply labels to counts
    polygon.define_label()

    # export point result
    export_data(output_path, polygon.point_label)

    # plot
    plot.add_polygon(polygon.x_values, polygon.y_values)
    for i in range(len(input_points.points)):
        plot.add_line(input_points.ray_lines[i][0][0], input_points.ray_lines[i][1][0],
                      input_points.ray_lines[i][0][1], input_points.ray_lines[i][1][1])
        plot.add_point(input_points.points[i][0], input_points.points[i][1], kind=polygon.point_label[i])
    plot.show()


if __name__ == '__main__':
    main(POLYGON CSV HERE,
         OUTPUT CSV HERE)
