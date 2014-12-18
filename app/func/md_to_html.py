import markdown
def md_to_html(filepath):
	unparsed_fileobj = open(filepath, "r")
	unparsed_text = unparsed_fileobj.read()
	unparsed_text = unparsed_text.split("\n")
	firstline = unparsed_text[0]
	title = unparsed_text[1]
	slidetitle = unparsed_text[2]
	unparsed_text = "\n".join(unparsed_text[3:])
	html = markdown.markdown(unparsed_text, extensions=["codehilite"])
	return {"firstline" : firstline, "title" : title, "slidetitle" : slidetitle, "slidecontent" : html}
