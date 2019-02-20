from flask import Flask, request, render_template, redirect, url_for
from flask import g
import os
import requests, json

app = Flask(__name__)
ctx = app.app_context()
ctx.push()


@app.route('/hello')
def hello():
    return 'Hello World!'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/user')
def user():
    r = requests.get('https://hunter-todo-api.herokuapp.com/user')
    return r.text


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/create_user', methods=['post'])
def create_user():
    username = request.form['username']
    r = requests.get('https://hunter-todo-api.herokuapp.com/user')
    exist_users = json.loads(r.text)
    for u in exist_users:
        if u['username'] == username:
            return 'user exists'
    r = requests.post('https://hunter-todo-api.herokuapp.com/user', data=json.dumps({'username': username}))
    return render_template('login.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_user', methods=['post'])
def login_user():
    username = request.form['username']
    r = requests.post('https://hunter-todo-api.herokuapp.com/auth', data=json.dumps({'username': username}))
    if r.status_code == 200:
        g.cookies = r.cookies
        return redirect('/todo-item')
    else:
        return 'login error'

@app.route('/todo-item')
def todo_item():
    r = requests.get('https://hunter-todo-api.herokuapp.com/todo-item', cookies=g.cookies)
    return render_template('todo-item.html', todo_item = r.text)

@app.route('/new-item')
def new_item():
    return render_template('new-item.html')

@app.route('/create-item', methods=['post'])
def create_item():
    content = request.form['content']
    r = requests.post('https://hunter-todo-api.herokuapp.com/todo-item', data=json.dumps({'content': content}), cookies=g.cookies)
    return redirect('/todo-item')

@app.route('/completed-item', methods=['post'])
def completed_item():
    r = requests.post('https://hunter-todo-api.herokuapp.com/todo-item',data=json.dumps({'completed':True}),cookies=g.cookies)
    return redirect('/todo-item')

@app.route('/delete-item', methods=['post'])
def delete_item():
    r = requests.post('https://hunter-todo-api.herokuapp.com/todo-item',data=json.dumps({'delete':True}),cookies=g.cookies)
    return redirect('/todo-item')

@app.route('/test')
def test():
    return redirect(url_for('hello'))

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host="0.0.0.0", port=port, threaded=True,debug=True)
