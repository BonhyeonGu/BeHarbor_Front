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

#로그인 페이지
@app.route("/login")
def login():
	if 'no' in session:
		return redirect(url_for('home'))
	return render_template('login.html')

#로그인 페이지 sql문 수정
@app.route("/login_back", methods=['POST'])
def login_back():
	inp_id = request.form['id']
	inp_pw = request.form['pw']
	sql = "SELECT EXISTS (SELECT id FROM Student WHERE id = %s LIMIT 1) AS SUCCESS;"
	cur.execute(sql, (inp_id))
	res = cur.fetchall()[0]
	if(res[0] == 0):
		return redirect(url_for('fail_login'))
	sql = "SELECT no, pw, name FROM Student WHERE id = %s"
	cur.execute(sql, (inp_id))
	q_no, q_pw, q_name = cur.fetchall()[0]
	q_pw = q_pw.encode('utf-8')
	if inp_id == '47262631':
		if not bcrypt.checkpw(inp_pw.encode('utf-8'),q_pw):
			return redirect(url_for('fail_login'))
		else:
			# session['name'] = q_name
			session['no'] = q_no
			session['id'] = inp_id
			session['name'] = q_name
			return redirect(url_for('harbor_manage_admin'))

	if not bcrypt.checkpw(inp_pw.encode('utf-8'), q_pw):
		return redirect(url_for('fail_login'))
	session['no'] = q_no
	session['id'] = inp_id
	session['name'] = q_name
	
	return render_template('home.html', user_name=q_name)

#생각난건데 로그인 실패 페이지 띄울때 세션 삭제하고 return하는게 더 안전한가요? 아님 그냥 해도 상관없나요
#로그아웃(세션삭제)
@app.route("/logout")
def logout():
	if not 'no' in session:
		return redirect(url_for('home'))
	session.clear()
	return redirect(url_for('home'))
#로그인 실패
@app.route("/fail_login")
def fail_login():
	return render_template('fail_login.html')

#관리자 페이지
@app.route("/harbor_manage_admin")
def harbor_manage_admin():
	if not 'no' in session:
		return redirect(url_for('login'))
	return render_template('admin.html', user_name = session['name'])


#공지페이지
@app.route("/notice")
def notice():
	if not 'no' in session:
		return redirect(url_for('login'))
	return render_template('notice.html', user_name=session['name'])

#홈화면
@app.route("/home")
def home():
	if not 'no' in session:
		return redirect(url_for('login'))
	return render_template('home.html', user_name=session['name'])

#ide서비스(쿠버네티스 주피터로 변경)
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
	return render_template('signup.html')

#파일 업로드
@app.route("/file_setting")
def file_setting():
	if not 'no' in session:
		return redirect(url_for('login'))
	u = Util()
	location = app.config['UPLOAD_FOLDER'] + session['id']
	names, dates_edit = u.outDirList(location)
	return render_template('file_setting.html', names=names, dates_edit=dates_edit, use=u.outDirByte(location))

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

#회원가입(admin계정 페이지)
@app.route("/signup")
def signupFront():
	return render_template('signup.html')

@app.route("/signup_back", methods=['POST'])
def signupBack():
	uname = request.form['name']
	uid = request.form['id']
	upw = request.form['pw']
	ugrade = request.form['grade']
	umajor = request.form['major']
	sql = "INSERT INTO Student (id, pw, name, grade, major) VALUES(%s, %s, %s, %s, %s)"
	encodeupw = bcrypt.hashpw(upw.encode('utf-8'), bcrypt.gensalt()) #encodeupw==> 암호화된 비번을 저장하는 변수
	#c는 입력받은 로그인 비번
	#bcryt.checkpw(c.encode('utf-8'),encodeupw)이런씩으로 확인하면 됩니당
	cur.execute(sql,(uid, encodeupw.decode('utf-8'), uname, ugrade, umajor))
	db.commit()
	return redirect(url_for('signupFront'))

if __name__ == "__main__":
	app.debug = True
	app.run(debug=True)