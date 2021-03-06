import os

from flask import render_template, redirect, request, session, g
from flask.ext.login import LoginManager, current_user, login_user, login_required

from app import app
from app.func import md_to_html
from .forms import *
from app.db import actions


app.config.from_object('config')
login_manager = LoginManager()
login_manager.init_app(app)
root_dir = str(__file__[:-13])




def is_user_ownpage(username, content):
    if g.user.is_authenticated():
        if username == g.user["username"]:
            content["ownpage"] = True
        else:
            content["ownpage"] = False



@login_manager.user_loader
def load_user(userid):
    return User.get(userid)


@app.before_request
def before_req():
    g.user = current_user


@app.route('/login', methods=['GET', 'POST'])
def login():
    content = dict()
    content["pagetype"] = "user_actions"
    content["action_type"] = "login"
    form = LoginForm()
    search = IndexForm()
    user_info = dict()
    if request.method == 'POST':
        if form.validate_on_submit():
            user_info["username"] = form.userid.data
            user_info["password"] = form.password.data
            if actions.auth_user(user_info)[0]:
                login_user(user_info["username"])
                g.user.update(actions.get_user_details(user_info["username"]))
                return redirect('/' + user_info["username"])
            else:
                content["error"] = "Invalid username or password"
        else:
            content["error"] = "Invalid data in field"
    return render_template('base.html', form=form, content=content, search=search)


@app.route('/logout')
@login_required
def logout():
    if 'logged_in' in session:
        del session['logged_in']
    return redirect('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    content = dict()
    form = SignupForm()
    search = IndexForm()
    if request.method == 'POST':
        user_info = dict()
        if form.validate_on_submit():
            user_info["username"] = form.username.data
            user_info["password"] = form.password.data
            user_info["email"] = form.email.data
            if not actions.sign_up_user(user_info)[0]:
                content["error"] = actions.sign_up_user(user_info)[1]
                return render_template('signup.html', content=content, form=form, search=search)
            else:
                return redirect('/' + user_info["username"])
    return render_template('signup.html', content=content, form=form, search=search)


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def root():
    content = dict()
    search = IndexForm()
    if request.method == 'POST':
        if search.validate_on_submit():
            content["result"] = actions.search_user_and_pres(search.search.data)
            return render_template('search.html', content=content, search=search)
    return render_template('index.html', content=content, search=search)



@app.route('/<username>/p/<presentation_name>')
@app.route('/<username>/p/<presentation_name>/<int:slide_number>')
def present(username, presentation_name, slide_number=1):
    prev_temp = 0
    content = dict()
    search = IndexForm()
    content["presentation_content"] = md_to_html.md_to_html(
        root_dir + "/presentations/" + str(username) + "/" + str(presentation_name) + "/" + str(slide_number) + ".md")
    for elem in os.listdir(root_dir + "/presentations/" + str(username) + "/" + str(presentation_name)):
        temp = elem[:-3]
        temp = int(temp)
        if temp > prev_temp:
            content["number_of_slides"] = temp
        prev_temp = temp
    content["presentation_name"] = presentation_name
    content["slide_number"] = slide_number
    content["next_page_link"] = str(presentation_name) + "/" + str(slide_number + 1)
    return render_template('presentation.html', content=content, search=search)

@app.route('/<username>/list')
def list_pres(username):
    content = dict()
    search = IndexForm()
    pres_names = os.listdir(root_dir + "/presentations/" + str(username))
    content["presentation_list"] = pres_names
    content["current_page_username"] = str(username)
    return render_template('list.html', content=content, search=search)

@app.route('/<username>/editor')
def editor(username):
    content = dict()
    form = MDEditor()
    content["current_page_username"] = username
    return render_template('editor.html', content=content, form=form)


@app.route('/<username>')
def user_page(username):
    user_info = actions.get_user_details(username)
    content = dict()
    search = IndexForm()
    content["current_page_username"] = username
    pres_list = os.listdir(root_dir + "/presentations/" + str(username))
    content["presentation_links"] = pres_list
    is_user_ownpage(username, content)
    return render_template('user_page.html', content=content, user_info=user_info, search=search)

