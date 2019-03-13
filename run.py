from flask import Flask, request, render_template, redirect, url_for, make_response
import os
import requests, json

app = Flask(__name__)

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
    jar = r.cookies
    print("cookiejar object: ", jar)

    #store info in a cookie
    response = make_response(redirect("/todo-item"))
    response.set_cookie('sillyauth', jar['sillyauth'])
    response.set_cookie('username', username)
    return response


@app.route('/todo-item',methods = ['GET','POST'])
def todo_item():
    #retrieved info from cookies
    val = request.cookies.get('sillyauth')
    jary = requests.cookies.RequestsCookieJar()
    jary.set('sillyauth', val, domain="hunter-todo-api.herokuapp.com")

    r = requests.get('https://hunter-todo-api.herokuapp.com/todo-item', cookies=jary)
    return render_template('todo-item.html', todo_item = r.json())

@app.route('/new-item')
def new_item():
    return render_template('new-item.html')

@app.route('/create-item', methods=['post'])
def create_item():
    #retrieved info from cookies
    val = request.cookies.get('sillyauth')
    jary = requests.cookies.RequestsCookieJar()
    jary.set('sillyauth', val, domain="hunter-todo-api.herokuapp.com")

    content = request.form['content']
    r = requests.post('https://hunter-todo-api.herokuapp.com/todo-item', data=json.dumps({'content': content}), cookies=jary)
    return redirect('/todo-item')

@app.route('/completed-item/<id>')
def completed_item(id):
    #retrieved info from cookies
    val = request.cookies.get('sillyauth')
    jary = requests.cookies.RequestsCookieJar()
    jary.set('sillyauth', val, domain="hunter-todo-api.herokuapp.com")

    r = requests.put('https://hunter-todo-api.herokuapp.com/todo-item/' + id,data=json.dumps({'completed':True}),cookies=jary)
    return redirect('/todo-item')

@app.route('/delete-item/<id>')
def delete_item(id):
    #retrieved info from cookies
    val = request.cookies.get('sillyauth')
    jary = requests.cookies.RequestsCookieJar()
    jary.set('sillyauth', val, domain="hunter-todo-api.herokuapp.com")

    r = requests.delete('https://hunter-todo-api.herokuapp.com/todo-item/' + id,data=json.dumps({'delete':True}),cookies=jary)
    return redirect('/todo-item')

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host="0.0.0.0", port=port, threaded=True,debug=True)
