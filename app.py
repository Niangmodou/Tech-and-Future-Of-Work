from flask import Flask, render_templates

@app.route('/')
def home():
	return render_templates('index.html')
	
if __name__ == "__main__":
	app.run()
