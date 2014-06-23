from flask import Flask
import subprocess
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "my_tumble_log"}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"


db = MongoEngine(app)
from flasky.models import Video

@app.route('/<id>')
def hello_world(id):
	vid=Video.objects.all()
	for v in vid:
		if v.vid==id and len(v.url)>5:
			return v.url
	output = subprocess.check_output(["youtube-dl", "-g", id])
	video=Video(title="id", vid=id, url=output)
	video.save()
	return output
    # output = subprocess.check_output(["youtube-dl", "-g", id]) 
    # return output

@app.route('/image/<id>')
def hello_img(id):
	#video=Video(title="id", vid="id")
	#video.save()
	vid=Video.objects.all()
	for v in vid:
		print v.id
		print v.url
		if v.vid==id and len(v.url)>5:
			return v.url
	output = subprocess.check_output(["youtube-dl", "-g", id])
	video=Video(title="id", vid=id, url=output)
	video.save()
	return output

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
