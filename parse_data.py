s = ""
with open("data.txt", mode="r", encoding="utf-8") as file:
	for line in file:
		s += line
build_dict = {}

i = 1
while i < len(s):
	assert s[i] == "'"
	cur_file = s[i + 1: s.index("'", i + 1)]
	i = s.index("'", i + 1)
	assert s[i: i + 23] == "': {<function Features.", s[i: i + 23]
	i += 4
	feat_to_val = {}
	while s[i] != "}":
		i += 19
		func = s[i: s.index(" ", i)]
		i = s.index(" ", i)
		assert s[i: i + 6] == ' at 0x', s[i: i + 6]
		i = s.index(":", i)
		i += 2
		# char_to_stop = ',' if s.find(",") != else '}'
		char_to_stop = '}' if s.find('}', i) < (s.find(',') if s.find(',') != -1 else len(s)) else ','
		val = s[i: s.index(char_to_stop, i)]
		i = s.index(char_to_stop, i)
		# print("",end="char_to_stop: " + char_to_stop if val[-1] != "," else "")
		feat_to_val[func] = float(val) if val[-1] != "}" else float(val[:-1])
	build_dict[cur_file] = feat_to_val
	if s[i: i + 23] == "}, 'tesserae/texts/grc/":
		i += 3
	else:
		assert s[i: i + 2] == '}}'

print(build_dict)