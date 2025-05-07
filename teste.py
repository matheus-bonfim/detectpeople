import ast
ch = {}

def a(ch):

    for i in range(10):
        ch[f'a{i}'] = i

a(ch)

str = '[1,2,3]'

print(str)
print(type(ast.literal_eval(str)))