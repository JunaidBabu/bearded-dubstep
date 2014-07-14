from flask import Flask
import subprocess
import time
from flask.ext.mongoengine import MongoEngine
from flask import request
import json

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "my_tumble_log"}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"


db = MongoEngine(app)
from flasky.models import Video

def extract(raw_string, start_marker, end_marker):
    start = raw_string.index(start_marker) + len(start_marker)
    end = raw_string.index(end_marker, start)
    return raw_string[start:end]


@app.route('/v/<id>')
def home(id):
	vid=Video.objects.all()
	output = "expire="+str(time.time())+"&"
	for v in vid:
		if v.vid==id and len(v.url)>5:
			try:
				exptime = extract(v.url, "expire=", "&")
			except:
				break
			print "exp "+ str(exptime)
			print "cur "+ str(time.time())
			if float(exptime)-float(time.time()) > 0:
				print float(exptime)-float(time.time())
				print "Returning "+v.url
				return v.url
			else:
				try:
					output = subprocess.check_output(["youtube-dl", "-g", id])
					Video.objects.filter(vid=v.vid).update(set__url=output)
				except:
					pass
				return output
			break
	try:
		output = subprocess.check_output(["youtube-dl", "-g", id])
	except:
		pass
	video=Video(title="id", vid=id, url=output)
	try:
		video.save()
	except:
		Video.objects.filter(vid=id).update(set__url=output)
	return output

@app.route('/cache', methods=['GET', 'POST'])
def login():
	#print request.args.get('obj', '')

	d = json.loads(request.args.get('obj', ''))
	for vid in d:
		print home(vid)
	return "True"

@app.route('/old/<id>')
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
