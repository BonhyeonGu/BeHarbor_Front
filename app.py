import bcrypt
from flask import Flask, render_template, request, session, jsonify, redirect, url_for
import pymysql
from flask_bcrypt import Bcrypt

from sub.secret import Secret

app = Flask(__name__)
app.secret_key = Secret.session_secret_key
db = pymysql.connect(host=Secret.db_host, port=Secret.db_port, user=Secret.db_user, passwd=Secret.db_passwd, db=Secret.db_name, charset='utf8')
cur = db.cursor()

@app.route("/")
def root():
	return redirect(url_for('/home_front'))

@app.route("/home")
def home_front():
	if 'name' in session:
		return render_template('home.html', user_name=session['no'])
	return render_template('home.html', user_name='NULL')

@app.route("/login_back", methods=['POST'])
def login_back():
	inp_id = request.form['id']
	inp_pw = request.form['pw']
	sql = "SELECT EXISTS (SELECT id FROM users WHERE id = %s LIMIT 1) AS SUCCESS;"
	cur.execute(sql, (inp_id))
	res = cur.fetchall[0]
	if(res == 0):
		return redirect(url_for('/fail'))
	sql = "SELECT no, pw, name FROM users WHERE id = %s"
	cur.execute(sql, (inp_id))
	q_no, q_pw, q_name = cur.fetchall()
	if not bcrypt.checkpw(q_pw, inp_pw):
		return redirect(url_for('/fail'))
	session['no'] = q_no
	session['name'] = q_name
	return render_template('home.html', user_name=q_name)

@app.route("/logout")
def logout():
	if not 'no' in session:
		return redirect(url_for('/home'))
	session.clear()
	return redirect(url_for('/home'))

@app.route("/fail")
def fail():
	if 'no' in session:
		return redirect(url_for('/home'))
	return render_template('')

@app.route("/ide")
def ide():
	if not 'no' in session:
		return redirect(url_for('/home'))
	url = 'http://' + Secret.ip_addr + str(Secret.ide_port + int(session['no']))
	return redirect(url)

@app.route("/upload")
def upload():
	if not 'no' in session:
		return redirect(url_for('/home'))
	return render_template('home.html', user_name='NULL')

@app.route("/signup_front")
def signupFront():
	return render_template('signup.html')

@app.route("/signup_back", methods=['POST'])
def signupBack():
	uid = request.form['uid']
	upw = request.form['upw']
	sql = "INSERT INTO Users (id, pw) VALUES(%s,%s)"
	encodeupw = bcrypt.hashpw(upw.encode('utf-8'),bcrypt.gensalt()) #encodeupw==> 암호화된 비번을 저장하는 변수
	#c는 입력받은 로그인 비번
	#bcryt.checkpw(c.encode('utf-8'),encodeupw)이런씩으로 확인하면 됩니당
	cur.execute(sql,(uid,encodeupw))
	db.commit()
	return render_template('signup.html') 

@app.route("/join_front")
def joinFront():
	return render_template('join.html')

@app.route("/join_back", methods=['POST'])
def post():
	#uid = request.form['input']
	#upw = ['김치 만드는법', '오늘의 과자', '유행하고 있는 과일', '맛있는 초콜릿']
	uid = request.form['uid']
	upw = request.form['upw']
	sql = "INSERT INTO Users (id, pw) VALUES(%s,%s)"
	cur.execute(sql,(uid, upw))
	db.commit()
	return render_template('main.html')
	#return render_template('output.html', value = value, value2 = value2)

@app.route("/go_out", methods=['POST'])
def goOut():
	print(request.is_json)#받아온게 json?
	j = request.json#main->string=>json->j
	print(j['name'])
	return render_template('out.html')

@app.route("/want*", methods=['POST'])
def want():
	name = "abc"
	old = 10
	test_data = {"name" : name, "old" : old}
	return jsonify(test_data)

if __name__ == "__main__":
	app.debug = True
	app.run(debug=True)