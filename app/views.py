from app import app
from flask import render_template
from app.func import md_to_html


def wrap_tags(content, tag):
	return "<" + str(tag) + ">" + str(content) + "</" + str(tag) + ">"



@app.route('/')
@app.route('/index')
def root():
	from os import listdir
	content = []
	for elem in listdir("presentations"):
		temp = "<a href=\"" + "/" + str(elem) +"\">" + str(elem) + "</a>"   
		content.append(wrap_tags(temp, "h5"))
	content = "\n".join(content)
	return render_template('index.html', content=content)

@app.route('/<presentation_name>')
@app.route('/<presentation_name>/<slide_number>')
def present(presentation_name, slide_number=1):
	slide = slide_number
	content = md_to_html.md_to_html("C:\Users\Dhash\Documents\GitHub\Flask-apps\\" + "presentations\\" + str(presentation_name) + "\\" + str(slide_number) + ".md")
	if content["firstline"] == "title":
		return render_template('Title.html', content=content)
	elif content["firstline"] == "heading":
		return render_template('Heading.html', content=content)
	elif content["firstline"] == "slide" or "":
		return render_template('Slide.html', content=content)