import markdown as md
import re

def markdown(str: str)-> str :
	res = md.markdown(str).replace("<li>","\t<li>")
	return res

def add_indent(str: str)-> str:
	row = str.splitlines()
	idx = 0 if row[0] != "" else 1
	indent = re.match("\s+",row[idx]).group()
	row[idx+1:] = list(map(lambda x: indent + x ,row[idx+1:]))
	return "\n".join(row)