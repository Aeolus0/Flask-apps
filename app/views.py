from app import app
from flask import render_template
from app.func import md_to_html
import os

def wrap_tags(content, tag):
	return "<" + str(tag) + ">" + str(content) + "</" + str(tag) + ">"
root_dir = str(os.getcwd())

@app.route('/')
@app.route('/index')
def root():
	content = []
	for elem in os.listdir("presentations"):
		temp = "<a href=\"" + "/" + str(elem) +"\">" + str(elem) + "</a>"   
		content.append(wrap_tags(temp, "h5"))
	content = "\n".join(content)
	return render_template('index.html', content=content)

@app.route('/<presentation_name>')
@app.route('/<presentation_name>/<int:slide_number>')
def present(presentation_name, slide_number=1):
	content = md_to_html.md_to_html(root_dir + "/presentations/" + str(presentation_name) + "/" + str(slide_number) + ".md")
	for elem in os.listdir("presentations/" + str(presentation_name)):
		temp = elem[:-3]
		temp = int(temp)
		prev_temp = 0
		if temp > prev_temp:
			content["number_of_slides"] = temp
		prev_temp = temp
	content["presentation_name"] = presentation_name
	content["slide_number"] = slide_number
	content["slidetitle"] = wrap_tags(content["slidetitle"], "h1")
	content["next_page_link"] = "/presentations/" + str(presentation_name) +"/" + str(slide_number + 1)
	if content["firstline"] == "title":
		return render_template('Title.html', content=content)
	elif content["firstline"] == "heading":
		return render_template('Heading.html', content=content)
	elif content["firstline"] == "slide" or "":
		return render_template('Slide.html', content=content)