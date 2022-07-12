import bcrypt
from flask import Flask, render_template, request, session, redirect, url_for
import pymysql
from werkzeug.utils import secure_filename

from sub.secret import Secret
from util import Util

app = Flask(__name__)
app.secret_key = Secret.session_secret_key
db = pymysql.connect(host=Secret.db_host, port=Secret.db_port, user=Secret.db_user, passwd=Secret.db_passwd, db=Secret.db_name, charset='utf8')
cur = db.cursor()

@app.route("/")
def root():
	return redirect(url_for('login'))

@app.route("/login")
def login():
	if 'no' in session:
		return redirect(url_for('home'))
	return render_template('login.html')

@app.route("/login_back", methods=['POST'])
def login_back():
	inp_id = request.form['id']
	inp_pw = request.form['pw']
	sql = "SELECT EXISTS (SELECT id FROM users WHERE id = %s LIMIT 1) AS SUCCESS;"
	cur.execute(sql, (inp_id))
	res = cur.fetchall[0]
	if(res == 0):
		return redirect(url_for('fail_login'))
	sql = "SELECT no, pw, name FROM users WHERE id = %s"
	cur.execute(sql, (inp_id))
	q_no, q_pw, q_name = cur.fetchall()
	if not bcrypt.checkpw(q_pw, inp_pw):
		return redirect(url_for('fail_login'))
	session['no'] = q_no
	session['name'] = q_name
	return render_template('home.html', user_name=q_name)

@app.route("/logout")
def logout():
	if not 'no' in session:
		return redirect(url_for('home'))
	session.clear()
	return redirect(url_for('home'))

@app.route("/fail_login")
def fail_login():
	if 'no' in session:
		return redirect(url_for('home'))
	return render_template('fail_login.html')

@app.route("/home")
def home():
	if not 'no' in session:
		return redirect(url_for('login'))
	return render_template('home.html', user_name=session['name'])

@app.route("/ide")
def ide():
	if not 'no' in session:
		return redirect(url_for('login'))
	url = 'http://' + Secret.ip_addr + str(Secret.ide_port + int(session['no']))
	return redirect(url)

@app.route("/file_setting")
def file_setting():
	if not 'no' in session:
		return redirect(url_for('login'))
	location = Secret.workspace + session['id']
	return render_template('file_setting.html', files=Util.outDirList(location), use=Util.outDirByte(location))

@app.route("/upload_back", methods=['POST'])
def upload_back():
	if not 'no' in session:
		return redirect(url_for('login'))
	location = Secret.workspace + session['id']

	file = request.files['file']
	file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
	return redirect(url_for('file_setting'))

@app.route("/signup_front")
def signupFront():
	return render_template('signup.html')

@app.route("/signup_back", methods=['POST'])
def signupBack():
	uid = request.form['uid']
	upw = request.form['upw']
	sql = "INSERT INTO users (id, pw) VALUES(%s,%s)"
	encodeupw = bcrypt.hashpw(upw.encode('utf-8'),bcrypt.gensalt()) #encodeupw==> 암호화된 비번을 저장하는 변수
	#c는 입력받은 로그인 비번
	#bcryt.checkpw(c.encode('utf-8'),encodeupw)이런씩으로 확인하면 됩니당
	cur.execute(sql,(uid,encodeupw))
	db.commit()
	return redirect(url_for('signupFront'))

if __name__ == "__main__":
	app.debug = True
	app.run(debug=True)