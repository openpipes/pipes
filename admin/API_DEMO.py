import hashlib
import json
import logging
from werkzeug import secure_filename
import os
from flask import Flask, request, redirect, url_for,make_response,jsonify,render_template
from werkzeug import secure_filename, SharedDataMiddleware
import sys
sys.path.append('/root/nb')
import PolicyReader as pr
from pypinyin import pinyin, lazy_pinyin

ALLOWED_EXTENSIONS_1 = set(['html','pdf','doc','docx','txt'])
ALLOWED_EXTENSIONS_2 = set(['excel'])

if os.path.isdir("./temp"):
    pass
else:
    os.mkdirs("./temp")
UPLOAD_FOLDER = './temp' 
app = Flask(__name__)


def allowed_file_1(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS_1
def allowed_file_2(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS_2

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
            files = request.files['filelists']
            data_file = request.files['excel']
            if file and allowed_file(file.filename):
#                 filename = hashlib.md5(file.filename.encode(encoding='UTF-8')).hexdigest()
                filename = "".join(lazy_pinyin(file.filename))
                filename = secure_filename(filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                doc = pr.read(app.config['UPLOAD_FOLDER']+'/'+filename)
                doc.summary()
                res = {"Keywords":top_kw(doc,10)}
                for each in doc.countObjects: res[each[0]] = each[1]
                    
                return render_template("docInfo.html",result = res)
            else:
                resp = jsonify({'message' : 'Allowed file types are html,pdf,doc,docx,txt'})
                resp.status_code = 400
                return resp             
    return '''    
    <!doctype html>
    <title style="text-align: center">Upload new File</title>  
    <h1 style="text-align: center">Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=excelfile>
         <input type=submit value=Upload>
    </form>
    '''
    

def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=5568)
#     host="0.0.0.0"
