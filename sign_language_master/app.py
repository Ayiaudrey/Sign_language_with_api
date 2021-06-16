from flask import Flask
import os
import urllib.request
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
import subprocess

UPLOAD_FOLDER = '/Users/imacoda10/Desktop/sign-language qui marche/audrey'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','mp4','avi','mov'])


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/file-upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = "nice.mp4"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #resp = jsonify({'message' : 'File successfully uploadeds'})
        #resp.status_code = 201
        #return resp
 
        print('********************Demarrage***************************')
        process = subprocess.Popen(['python' , '/Users/imacoda10/Desktop/sign-language qui marche/livedemo1.py' ], stdout=subprocess.PIPE)
        out, err = process.communicate()
        out = out.decode("ascii").rstrip()
        output=out[150:]
        print(output)
        json=jsonify({"reponse":output})
        return json
    
    else:
        resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp


        
"""@app.route('/response', methods=['POST', 'GET'])
def launch_script():
    print('********************Demarrage***************************')
    process = subprocess.Popen(['python' , '/Users/imacoda10/Desktop/sign-language qui marche/livedemo1.py' ], stdout=subprocess.PIPE)
    out, err = process.communicate()
    out = out.decode("ascii").rstrip()
    json=jsonify({"reponse":out})
    #print(out)
    return json"""

if __name__== "__main__":
    app.run(debug = True)