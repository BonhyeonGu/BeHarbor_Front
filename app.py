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
	return redirect(url_for('home'))

#홈화면
@app.route("/home")
def home():
	return render_template('home.html')

#로그인 페이지
@app.route("/login")
def login():
	return render_template('login.html')

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

#관리자 페이지//관리자 계정만 로그인 가능
@app.route("/harbor_manage_admin")
def harbor_manage_admin():
	if not 'no' in session:
		return redirect(url_for('login'))
	if session['id'] != "47262631":
		return redirect(url_for('login'))
	return render_template('admin.html')

#쿠버네티스 서비스 페이지 
@app.route("/kuber_url")
def kuber_url():
	return render_template('kuber_url.html')

@app.route("/kuber_url_back")
def kuber_url_back():
	return (url_for('kuber_url'))

#일반 공개 공지 페이지
@app.route("/notice")
def notice():
	sql = "select n.no, s.name, n.headline, n.join_date from Student s, Notice n where s.id = n.sno"
	cur.execute(sql)
	notices = cur.fetchall()
	return render_template('notice_all_t.html',notices = notices)

#공지 관리 페이지(관리자 전용 페이지)
@app.route("/notice_admin")
def notice_admin():
	if not 'no' in session:
		return redirect(url_for('login'))
	if session['id'] != '47262631':
		return redirect(url_for('login'))
	sql = "select * from Notice;"
	#no, sno, notice, join_date
	cur.execute(sql)
	notices = cur.fetchall()
	return render_template('notice_admin.html',notices = notices)

#공지 추가(관리자 전용 페이지)
@app.route('/notice_add')
def notice_add():
	if not 'no' in session:
		return redirect(url_for('login'))
	if session['id'] != '47262631':
		return redirect(url_for('login'))
	return render_template('notice_add.html')

@app.route('/notice_add_back',methods=['POST'])
def notice_add_back():
	# sql = "SELECT s.id FROM Student s, notice n WHERE n.sno = s.id And n.sno = '1111';"
	sno = request.form['sno']
	notice = request.form['notice']
	headline = request.form['headline']
	sql = "INSERT INTO Notice (sno, headline, notice) VALUES(%s,%s,%s)"
	cur.execute(sql,(sno,headline, notice))
	db.commit()
	return redirect(url_for('notice_admin'))


@app.route('/notice_del_back',methods=['POST'])
def notice_del_back():
	no = request.form['no']
	# sql = "INSERT INTO Notice (sno, headline, notice) VALUES(%s,%s,%s)"
	sql = "DELETE FROM Notice where no = %s"
	cur.execute(sql,(no))
	db.commit()
	return redirect(url_for('notice_admin'))

#ide서비스 페이지(현재는 서비스 안됨)
@app.route("/ide")
def ide():
	if not 'no' in session:
		return redirect(url_for('login'))
	url = 'http://' + Secret.ip_addr + str(Secret.ide_port + int(session['no']))
	return redirect(url)

#css 테스트용 주소/ 개발할 때 주소 뒤에 /testt 붙여서 접속하면 따로 로그인할 필요없어요
#테스트할 파일을 바꾸고 싶으면 return 템플릿에서 community.html 대신 적용할 파일 적어주면 됩니다.
@app.route("/testt")
def testt():
	return render_template('home_test_YH.html')

#회원가입(admin계정 페이지)
@app.route("/signup")
def signup():
	if not 'no' in session:
		return redirect(url_for('login'))
	if session['id'] != '47262631':
		return redirect(url_for('login'))	
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
	return redirect(url_for('signup'))

#파일 업로드(서비스 미정)
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


if __name__ == "__main__":
	app.debug = True
	app.run(debug=True)