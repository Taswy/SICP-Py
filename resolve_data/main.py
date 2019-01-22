# code=utf-8

class Point(object):
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
    def tostring(self):
        return "{} {} ".format(self.x, self.y)

class Line(object):
    def __init__(self, id, p1_index, p2_index):
        self.id = id
        self.p1_index = p1_index
        self.p2_index = p2_index
    def tostring(self, processer, index):
        if index:
            return processer.points[0].tostring()
        return processer.points[1].tostring()

class LineLoop(object):
    def __init__(self, line_list):
        self.length = len(line_list)
        self.line_list = line_list
    def tostring(self, processer):
        bool_list = list(map(lambda x: x > 0, self.line_list))
        attr_list = [(processer.lines[abs(self.line_list[i])], bool_list[i]) for i in range(len(self.line_list))]
        str_list = [line.tostring(processer, index) for (line, index) in attr_list]
        return ''.join(str_list)

class Processer(object):
    def __init__(self):
        self.points = {}
        self.lines = {}
        self.line_loops = []

    def set_point(self, point):
        self.points[point.id] = point
    def set_line(self, line):
        self.lines[line.id] = line
    def set_line_loop(self, line_loop):
        self.line_loops.append(line_loop)

    def display(self):
        self.length_display()
        self.random_serial_display()
        self.points_display()

    def length_display(self):
        length_list = [line_loop.length for line_loop in self.line_loops]
        length_str = " ".join(list(map(str, length_list)))
        print(length_str)

    def random_serial_display(self):
        print("This is the random line.", len(self.line_loops), "elemtents.")

    def points_display(self):
        for line_loop in self.line_loops:
            print(line_loop.tostring(self))
            
