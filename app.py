from flask import Flask, render_template, request, session, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import hashlib
import jsonify
import os

app = Flask(__name__)

os.environ['DATABASE_URL'] = "postgresql://localhost/tech-future-of-work"
app.config.from_object(os.environ['APP_SETTINGS']) #Uncomment to push to heroku
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://ewxxbmmjueyovr:c9bd967c93c2c61fbf3ce12d8a220704418b22c88113f2a3d4ec91deedd03c7c@ec2-52-72-34-184.compute-1.amazonaws.com:5432/dfjqlg32idlchq"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import Student, Topic, Admin

SALT = 'TECH'

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/student', methods=['GET'])
def student():
	#Get available topics from # DB and pass it to the frontend
	try:
		topics = Topic.query.filter_by(status='True')

	except Exception as e:
		return str(e)

	return render_template('student.html', topics=topics)

'''
@app.route('/allStudents', methods=['GET'])
def get_students():
	#Get all students and their topics
	try:
		students = Student.query.all()
	except Exception as e:
		return str(e)

	return render_template('studentPage.html', students=students)
'''

@app.route('/postGroup', methods=['GET', 'POST'])
def post_group():
	if request.form:
		#Get data from frontend
		data = request.form

		#Get active students
		student_lst = []

		#Get current user
		name = data['name']
		netID = data['netId']

		student_lst.append((name, netID))

		topic = get_topic_name(data['topic'])

		#Get teammate 1
		teammate_name1 = ''
		teammate_netId1 = ''

		if data['name1'] != '' and data['netId1'] != '':
			teammate_name1 = data['name1']
			teammate_netId1 = data['netId1']

			student_lst.append((teammate_name1, teammate_netId1))

		#Get teammate 2
		teammate_name2 = ''
		teammate_netId2 = ''

		if data['name2'] != '' and data['netId2'] != '':
			teammate_name2 = data['name2']
			teammate_netId2 = data['netId2']

			student_lst.append((teammate_name2, teammate_netId2))

		#Get teammate 3
		teammate_name3 = ''
		teammate_netId3 = ''

		if data['name3'] != '' and data['netId3'] != '':
			teammate_name3 = data['name3']
			teammate_netId3 = data['netId3']

			student_lst.append((teammate_name3, teammate_netId3))

		#Retreive topics from frontend
		try:
			topics = Topic.query.filter_by(status = 'True')

		except Exception as e:
			return str(e)
		print('Selected Topic: ', topic)
		message = commit_database(student_lst, topic)

		return render_template('student.html', topics=topics, message = message)

#Function to add all students in the group and topic to DB
def commit_database(students, topic):
	#Check if all the netIDs has already been registered
	found = False

	#Search All students to check for duplicates
	for student in students:

		student_netId = student[1]
		if '@' in student_netId:
			message = 'Error: Please enter you netID(No @)'
			found = True
			break

		try:
			#If we have an existing student in our database
			if Student.query.filter_by(netId=student_netId).first():
				message = 'Error: Found an Existing Student'
				found = True
				break

		except Exception as e:
			return str(e)

	#Add new students to the database, since no duplicates
	if not found:
		try:
			#Update topic status to False
			topic_db = Topic.query.filter_by(name=topic).first()
			print(topic_db)

			setattr(topic_db, 'status', 'False')

			db.session.commit()

		except Exception as e:
			return str(e)


		for student in students:
			#Retrieve vital student information
			name = student[0]
			netId = student[1]
			first_name, last_name = get_first_last(name)

			try:
				#Creating a new student instance to add
				new_student = Student(
					netId = netId,
					first = first_name,
					last = last_name,
					topic = topic
				)

				db.session.add(new_student)
				db.session.commit()

				message = 'Students have been succesfully added'
			except Exception as e:
				return str(e)

	return message

#Seperate first and last name
def get_first_last(name):
	ind = name.find(' ')

	first_name = name[:ind]
	last_name = name[ind+1:]

	return (first_name, last_name)

#Parse out topic name
def get_topic_name(topic):
	colon = topic.find(':')
	comma = topic.find(',')

	name = topic[colon+2 : comma]

	return name

@app.route('/adminLogin')
def admin_login():
	return render_template('admin.html')

@app.route('/adminLoginAuth', methods=['GET', 'POST'])
def login_auth():
	if request.form:
		data = request.form

		#Get data from front end
		username = data['name']
		password = data['password'] + SALT
		print('1: ',username, password)

		password_hash = get_password_hash(password)
		print(password_hash)
		#Check if it matches with the database
		try:
			user = Admin.query.filter_by(username=username,
										 password=password_hash).first()
			if user != None:
				print('success')
				#if success match, we redirect to the home page for admin

				session['username'] = username
				return redirect(url_for('admin_home'))

			return render_template('admin.html', message = 'Invalid Credentials')

		except Exception as e:
			return str(e)



def get_password_hash(password):
	return hashlib.sha256(password.encode('utf-8')).hexdigest()

@app.route('/logout', methods=['POST'])
def logout():
	session.pop('username')

	return redirect('/')

@app.route('/admin_home', methods=['GET'])
def admin_home():
	try:
		json = {}

		#Get all topcs
		topics = Topic.query.all()

		#Get all students_json
		students = Student.query.all()

		for topic in topics:
			json[topic.name] = []

		#Find all students who belong to each topic and construct a dict
		for topic_name in json:
			students = Student.query.filter_by(topic=topic_name).all()

			json[topic_name] = students


		#print(students)
		print(json)
		#students_json = jsonify([s.serialize() for s in students])
		#print('Student: ', students_json)
		return render_template('users.html', data = json)

	except Exception as e:
		return str(e)

app.secret_key = 'some random key here. usually in env.'

if __name__ == "__main__":
	app.debug = True
	app.run()
