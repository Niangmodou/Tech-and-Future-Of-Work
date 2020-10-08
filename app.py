from flask import Flask, render_template, request, session, url_for, redirect

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/student')
def student():
	return render_template('student.html')

@app.route('/admin')
def admin_home():
	return render_template('admin.html')
'''
@app.route('/adminLoginAuth', methods=['POST'])
def login_auth():
	pass

@app.route('/adminLogin', methods=['GET'])
def login_auth():
	pass


@app.route('/postGroup', methods=['POST'])
def post_group():
	pass
'''

if __name__ == "__main__":
	app.run(debug=True)
