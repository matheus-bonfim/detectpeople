

def line_func(x1,y1,x2,y2):
    a = (y2 - y1)/(x2 - x1)
    b = y1 - a*x1
    return a, b

def dist_line_signed(x, y, a, b):
    A = a
    B = -1
    C = b
    return (A*x + B*y + C) / ((A**2 + B**2)**0.5)


x1, y1 = 0, 300
x2, y2 = 1280, 0

l_a, l_b = line_func(x1, y1, x2, y2)

ax, ay = 200, 150
bx, by = 800, 400

da = dist_line_signed(ax, ay, l_a, l_b)
db = dist_line_signed(bx, by, l_a, l_b)

#print("dist A: ",da)
#print("dist B: ",db)