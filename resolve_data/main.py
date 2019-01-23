# code=utf-8
import re

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
    start_line = "Lines & Boundaries"
    end_line = "Surfaces and physical entities"
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
            
    def read_obj(self, text_line):
        class_names = ["Point", "Line", "Line Loop"]
        [obj_str, data_str] = text_line.strip().split("=")
        obj_type = None
        for class_name in class_names:
            if class_name in obj_str:
                obj_type = class_name
        if not obj_type:
            return None
        pattern = re.compile(r'[(](.*?)[)]')
        obj_id = int(re.findall(pattern, obj_str))
        return obj_type, obj_id, data_str

    def set_obj(self, text_line):
        obj_context = self.read_obj(text_line)
        if obj_context is None:
            return
        (obj_type, obj_id, data_str) = obj_context
        pattern = re.compile(r'{.*?}')
        data_content_list = list(map(lambda s: s.strip(), re.findall(pattern, data_str).split(',')))
        if obj_type == "Point":
            (x, y) = tuple(map(float, data_content_list[0:2]))
            point = Point(obj_id, x, y)
            self.set_point(point)
        elif obj_type == "Line":
            (p1, p2) = tuple(map(int, data_content_list))
            line = Line(obj_id, p1, p2)
            self.set_line(line)
        else:
            line_list = list(map(int, data_content_list))
            line_loop = LineLoop(line_list)
            self.set_line_loop(line_loop)
