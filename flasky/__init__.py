from flask import Flask
import subprocess
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "my_tumble_log"}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"


db = MongoEngine(app)


@app.route('/<id>')
def hello_world(id):
    cmd = "/usr/sbin/netstat -p tcp -f inet"
    output = subprocess.check_output(["youtube-dl", "-g", id]) 
    return output

@app.route('/img/<id>')
def hello_img(id):
    return  

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
