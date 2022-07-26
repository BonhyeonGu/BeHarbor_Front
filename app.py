import bcrypt
from flask import Flask, render_template, request, session, redirect, url_for
import pymysql
from werkzeug.utils import secure_filename
#-----------------------------------------------------
from secret.secret import Secret
from util import Util
#-----------------------------------------------------
app = Flask(__name__)
app.secret_key = Secret.session_secret_key
db = pymysql.connect(host=Secret.db_host, port=Secret.db_port, user=Secret.db_user, passwd=Secret.db_passwd, db=Secret.db_name, charset='utf8')
cur = db.cursor()
#-----------------------------------------------------
app.secret_key = Secret.app_secret_key
app.config['UPLOAD_FOLDER'] = Secret.workspace
#-----------------------------------------------------
@app.route("/")
def root():
	session.clear()
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
	res = cur.fetchall()[0]
	if(res[0] == 0):
		return redirect(url_for('fail_login'))
	sql = "SELECT no, pw, name FROM users WHERE id = %s"
	cur.execute(sql, (inp_id))
	q_no, q_pw, q_name = cur.fetchall()[0]
	q_pw = q_pw.encode('utf-8')
	if not bcrypt.checkpw(inp_pw.encode('utf-8'), q_pw):
		return redirect(url_for('fail_login'))
	session['no'] = q_no
	session['id'] = inp_id
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

#css 테스트용 주소/ 개발할 때 주소 뒤에 /testt 붙여서 접속하면 따로 로그인할 필요없어요
#테스트할 파일을 바꾸고 싶으면 return 템플릿에서 community.html 대신 적용할 파일 적어주면 됩니다.
#파일업로드 페이지는 적용x 아이디 정보가 필요해서,,
@app.route("/testt")
def testt():
	return render_template('home.html')

@app.route("/file_setting")
def file_setting():
	if not 'no' in session:
		return redirect(url_for('login'))
	u = Util()
	location = app.config['UPLOAD_FOLDER'] + session['id']
	names, dates_edit = u.outDirList(location)
	return render_template('file_setting.html', names=names, dates_edit=dates_edit, use=u.outDirByte(location))

#파일 총 사용량 오류? 제대로 용량이 안 떠요
@app.route("/upload_back", methods=['POST'])
def upload_back():
	if not 'no' in session:
		return redirect(url_for('login'))
	u = Util()
	location = app.config['UPLOAD_FOLDER'] + session['id']
	use = u.outDirByte(location)
	if use > Secret.maxbyte:
		return redirect(url_for('file_setting'))
	file = request.files['file']
	
	file.save(u.pathJoin(location, file.filename))
	return redirect(url_for('file_setting'))

@app.route("/signup")
def signupFront():
	return render_template('signup.html')

@app.route("/signup_back", methods=['POST'])
def signupBack():
	uname = request.form['name']
	uid = request.form['id']
	upw = request.form['pw']
	sql = "INSERT INTO users (id, pw, name) VALUES(%s, %s, %s)"
	encodeupw = bcrypt.hashpw(upw.encode('utf-8'), bcrypt.gensalt()) #encodeupw==> 암호화된 비번을 저장하는 변수
	#c는 입력받은 로그인 비번
	#bcryt.checkpw(c.encode('utf-8'),encodeupw)이런씩으로 확인하면 됩니당
	cur.execute(sql,(uid, encodeupw.decode('utf-8'), uname))
	db.commit()
	return redirect(url_for('signupFront'))

if __name__ == "__main__":
	app.debug = True
	app.run(debug=True)