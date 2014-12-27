from app import app
from flask import render_template, redirect, request
from app.func import md_to_html
from .forms import *
from db import *
import os

app.config.from_object('config')

def wrap_tags(content, tag):
	return "<" + str(tag) + ">" + str(content) + "</" + str(tag) + ">"
root_dir = str(__file__[:-13])

@app.route('/')
@app.route('/index')
def root():
	content = []
	for elem in os.listdir(root_dir + "presentations"):
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
	if content["firstline"] == "title\r" or content["firstline"] == "title":
		return render_template('Title.html', content=content)
	elif content["firstline"] == "heading\r" or content["firstline"] == "heading":
		return render_template('Heading.html', content=content)
	elif content["firstline"] == "slide\r" or content["firstline"] == "" or content["firstline"] == "slide":
		return render_template('Slide.html', content=content)
	else:
		return render_template("Something_went_wrong.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
	import bcrypt
	content = {}
	form = LoginForm()
	user_info = {}
	if request.method == 'POST':
		if form.validate_on_submit():
			user_info["username"] = form.userid.data
			user_info["password"] = form.password.data
			if actions.auth_user(user_info):
				return redirect('/' + user_info["username"])
			else:
				content["loginfailure"] = "Invalid username or password"
		else:
			content["loginfailure"] = "Invalid data in field"
	return render_template('login.html', form=form, content=content)
