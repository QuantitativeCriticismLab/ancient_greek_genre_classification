import ast
s = ""
with open("data.txt") as file:
	for line in file:
		s += line
ast.literal_eval(s)
len(s)