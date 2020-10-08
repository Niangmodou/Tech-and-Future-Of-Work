from flask import Flask, render_template, request, session, url_for, redirect

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/student')
def student():
	#Get available topics from # DB and pass it to the frontend
	topics = ['Mixed Reality & the Metaverse',
			  'Quantum Computing',
			  'Nanotechnology or Nanobiotechnology',
			  'Bioprinting',
			  'Brain-machine interface',
			  'IoT & Cloud Computing',
			  'Autonomous Vehicles',
			  'Commercial UAV',
			  'Digital Fabrication',
			  'Blockchain']

	return render_template('student.html', topics=topics)

@app.route('/admin')
def admin_home():
	return render_template('admin.html')

@app.route('/postGroup', methods=['GET', 'POST'])
def post_group():
	if request.form:
		data = request.form
		#Get data from frontend
		name = data['name']
		netID = data['netId']

		topic = data['topic']


		#Check if netID has already been registered

		#Add to the database, if success
	pass

'''
@app.route('/adminLoginAuth', methods=['POST'])
def login_auth():
	pass

@app.route('/adminLogin', methods=['GET'])
def login_auth():
	pass

Mixed Reality & the Metaverse (AR/VR - Augmented & Virtual Reality)
Quantum Computing
Nanotechnology or Nanobiotechnology
Bioprinting
Brain-machine interface (e.g. Neuralink)
IoT & Cloud Computing
Autonomous Vehicles
Commercial UAV (advanced autonomous drones)
Digital Fabrication (laser cutting, CNC machining, 3D printing, etc.)
Blockchain
'''


if __name__ == "__main__":
	app.run(debug=True)
