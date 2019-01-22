# coding=utf-8

from operator import add, sub, mul,	truediv

"""
通过声明式的方法构造面向对象过程 -> 约束+连接器
使用消息传递系统来协调约束和连接器,不会使用函数来响应消息,而是使用字典。
当设定一个约束时，不仅对应连接器的值会改变，这种改变还会在整个网络中进行传播。
当一个连接器改变时，如果比如celsius获得了一个新的值，那么网络会将fahrenheit原来的值忘掉，这样就可以得出新的值了。
这个网络中的计算过程是无方向的，这是基于约束的网络的特征。
实现这个约束系统时，连接器就是字典，将消息名称映射为函数和数据值。
要实现的连接器如下：
    connector['set_val'](source,value)	 	表示 source	请求连接器将当前值设置为该值。
	connector['has_val']()	 	            返回连接器是否已经有了一个值。
	connector['val']	 	                返回连接器的当前值。
	connector['forget'](source)	 	        告诉连接器,	source　请求它忘掉当前值。
	connector['connect'](source)	 	    传播连接器参与新的约束 source 的消息。
约束也是字典,接受来自连接器的以下两种消息:
	constraint['new_val']()	 	            表示连接到约束的连接器有了新的值。
	constraint['forget']()	 	            表示连接到约束的连接器需要忘掉它
加法器和乘法器会自动根据三个值中的两个实现另外一个。
"""
def make_converter(c, f):
    """Connect c to f with constraints to convert from Celsius to Fahrenheit."""
    u, v, w, x, y = [make_connector() for _ in range(5)]
    multiplier(c, w, u)
    multiplier(v, x, u)
    adder(v, y, f)
    constant(w, 9)
    constant(x, 5)
    constant(y, 32)


def make_connector(name=None):
    """A connector between constraints"""
    informant = None # 连接器必须跟踪当前值的informant，以及它所参与的constraint列表
    constraints = []
    def set_value(source, value):
        nonlocal informant
        val = connector['val']
        if val is None:
            informant, connector['val'] = source, value
            if name is not None:
                print(name, '=', value)
            inform_all_except(source, 'new_val', constraints)
        else:
            if val != value:
                print('Contradiction detected:', val, 'vs', value )
    def forget_value(source):
        nonlocal informant
        if informant == source:
            informant, connector['val'] = None, None
            if name is not None:
                print(name, 'is forgotten')
            inform_all_except(source, 'forget', constraints)
    connector = {'val': None,
                 'set_val': set_value,
                 'forget': forget_value,
                 'has_val': lambda: connector['val'] is not None,
                 'connect': lambda source: constraints.append(source)}
    return connector

def adder(a, b, c):
    """The constrain that a + b = c"""
    return make_ternary_constraint(a, b, c, add, sub, sub)

def multiplier(a, b, c):
    """The constraint that a * b = c"""
    return make_ternary_constraint(a, b, c, mul, truediv, truediv)

def make_ternary_constraint(a, b, c, ab, ca, cb):
    """The constraint that ab(a, b)=c and ca(c, a)=b and cb(c, b)=a"""
    def new_value():
        av, bv, cv = [connector['has_val']() for connector in (a, b, c)]
        if av and bv:
            c['set_val'](constraint, ab(a['val'], b['val']))
        elif av and cv:
            b['set_val'](constraint, ca(c['val'], a['val']))
        elif bv and cv:
            a['set_val'](constraint, cb(c['val'], b['val']))
    def forget_value():
        for connector in (a, b, c):
            connector['forget'](constraint)
    constraint = {'new_val': new_value, 'forget': forget_value}  # 分发字典,也是约束对象自身
    for connector in (a, b, c):
        connector['connect'](constraint)
    return constraint

def constant(connector, value):
    """"The constraint that connector = value, without sending informant"""
    constraint = {}
    connector['set_val'](constraint, value)
    return constraint

def inform_all_except(source, mesage, constraints):
    """Inform all constraints of the message, except source."""
    for c in constraints:
        if c != source:
            c[mesage]()

celsius = make_connector('Celsius')
fahrenheit = make_connector('Fahrenheit')

make_converter(celsius, fahrenheit)

fahrenheit['set_val']('user', 212)
