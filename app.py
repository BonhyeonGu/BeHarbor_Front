from flask import Flask, render_template, request, session, jsonify
import pymysql

app = Flask(__name__)
app.secret_key = b'aaa!111/'
db = pymysql.connect(host='9bon.org', port=14406, user='flask', passwd='1234', db='flask', charset='utf8')
cur = db.cursor()
@app.route("/")
def start():
	uno = -1
	if 'user_no' in session:
		uno = session['user_no']
	print(uno)
	return render_template('main.html', value=uno)

@app.route("/login_front")
def loginFront():
	return render_template('login.html')
@app.route("/login_back", methods=['POST'])
def loginBack():
	uid = request.form['uid']
	upw = request.form['upw']
	sql = "SELECT uno, pw FROM Users WHERE id = %s"
	cur.execute(sql,(uid))
	sel = cur.fetchall()
	if upw==sel[0][1]:
		uno = sel[0][0]
		session['user_no'] = uno
		return render_template('main.html')
	else:
		return "알맞지 않음"	

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