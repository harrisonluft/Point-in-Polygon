from plotter import Plotter
from main_from_file import Poly
from main_from_file import Point


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


def export_data(path, eastings, northings, classification):
    id = []
    eastings_str = []
    northings_str = []
    n = 1
    for i in range(len(classification)):
        id.append(str(n+i))
        eastings_str.append(str(eastings[i][0]))
        northings_str.append(str(northings[i][1]))
    with open(path, "w") as f:
        f.write(','.join(['ID', 'eastings', 'northings', 'classifications', '\n']))
        for j in range(len(classification)):
            f.write(','.join([id[j], eastings_str[j], northings_str[j], classification[j], '\n']))


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


def main(polygon_path, input_points_path, output_path):
    plot = Plotter()

    # import data
    print("read polygon.csv")
    poly_points = import_data(polygon_path)
    print("read input.csv")
    points = import_data(input_points_path)

    print("categorize points")
    # assign classes
    ucl_polygon = Poly(poly_points)
    ucl_points = Point(points)

    # MBR
    ucl_polygon.mbr()

    # Generate Rays
    ucl_points.ray_lines(ucl_polygon.max_x)

    # RCA Classification
    ucl_polygon.rca_rays(ucl_points.ray_lines)
    ucl_polygon.rca_count()
    ucl_polygon.define_label()

    # export data
    print("write output.csv")
    export_data(output_path, ucl_points.points, ucl_points.points, ucl_polygon.point_label)

    print("plot polygon, points and rays")
    # plot
    plot.add_polygon(ucl_polygon.x_values, ucl_polygon.y_values)
    for i in range(len(ucl_points.points)):
        plot.add_point(ucl_points.points[i][0], ucl_points.points[i][1], kind=ucl_polygon.point_label[i])
    plot.show()

    # Incorporating Basemap
    test = import_data("C:/Users/17075/Assignment_1/Project Template/UCL_test_output.csv")
    print(test)


if __name__ == '__main__':
    main("C:/Users/17075/Assignment_1/Project Template/UCL_polygon.csv",
         "C:/Users/17075/Assignment_1/Project Template/UCL_test_points.csv",
         "C:/Users/17075/Assignment_1/Project Template/UCL_test_output.csv")

