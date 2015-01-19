import os

from flask import render_template, redirect, request, session, g
from flask.ext.login import LoginManager, current_user

from app import app
from app.func import md_to_html
from .forms import *
from app.db import actions


app.config.from_object('config')

login_manager = LoginManager()
login_manager.init_app(app)


def wrap_tags(content, tag):
    return "<" + str(tag) + ">" + str(content) + "</" + str(tag) + ">"


root_dir = str(__file__[:-13])

actions.create_database(root_dir)


@login_manager.user_loader
def load_user(userid):
    return User.get(userid)


@app.before_request
def before_req():
    g.user = current_user


@app.route('/login', methods=['GET', 'POST'])
def login():
    content = {}
    content["pagetype"] = "user_actions"
    content["action_type"] = "login"
    form = LoginForm()
    user_info = {}
    if request.method == 'POST':
        if form.validate_on_submit():
            user_info["username"] = form.userid.data
            user_info["password"] = form.password.data
            if actions.auth_user(user_info):
                login_user(user_info["username"])
                g.user.update(actions.get_user_details(user_info["username"]))
                return redirect('/' + user_info["username"])
            else:
                content["error"] = "Invalid username or password"
        else:
            content["error"] = "Invalid data in field"
    return render_template('base.html', form=form, content=content)


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        del session['logged_in']
    return redirect('/')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    content = {}
    content["pagetype"] = "user_actions"
    content["action_type"] = "signup"
    if request.method == 'POST':
        form = LoginForm()
        user_info = {}
        if form.validate_on_submit():
            user_info["username"] = form.userid.data
            user_info["password"] = form.password.data
            user_info["email"] = form.email.data
            data = actions.sign_up_user(user_info)
            if type(data) == "<type 'tuple'>":
                content["error"] = data[1]
            else:
                return redirect('/' + user_info["username"])
    return render_template('base.html', content=content)


@app.route('/')
@app.route('/index')
def root():
    content = []
    for elem in os.listdir(root_dir + "/presentations"):
        temp = "<a href=\"" + "/" + str(elem) + "\">" + str(elem) + "</a>"
        content.append(wrap_tags(temp, "h5"))
    content = "\n".join(content)
    return render_template('index.html', content=content)


@app.route('/<username>/p/<presentation_name>')
@app.route('/<username>/p/<presentation_name>/<int:slide_number>')
def present(username, presentation_name, slide_number=1):
    content = md_to_html.md_to_html(
        root_dir + "/presentations/" + str(username) + "/" + str(presentation_name) + "/" + str(slide_number) + ".md")
    for elem in os.listdir("presentations/" + str(username) + "/" + str(presentation_name)):
        temp = elem[:-3]
        temp = int(temp)
        prev_temp = 0
        if temp > prev_temp:
            content["number_of_slides"] = temp
        prev_temp = temp
    content["presentation_name"] = presentation_name
    content["slide_number"] = slide_number
    content["slidetitle"] = wrap_tags(content["slidetitle"], "h1")
    content["next_page_link"] = "/presentations/" + str(presentation_name) + "/" + str(slide_number + 1)
    if content["firstline"] == "title\r" or content["firstline"] == "title":
        return render_template('Title.html', content=content)
    elif content["firstline"] == "heading\r" or content["firstline"] == "heading":
        return render_template('Heading.html', content=content)
    elif content["firstline"] == "slide\r" or content["firstline"] == "" or content["firstline"] == "slide":
        return render_template('Slide.html', content=content)
    else:
        return render_template("Something_went_wrong.html")


@app.route('/<username>')
def user_page(username):
    user_info = actions.get_user_details(username)
    content = {}
    content["current_page_username"] = username
    pres_list = os.listdir("presentations/" + str(username))
    content["presentation_links"] = pres_list
    if g.user.is_authenticated():
        if username == g.user["username"]:
            content["ownpage"] = True
        else:
            content["ownpage"] = False
    return render_template('user_page.html', content=content, user_info=user_info)

