from flask import Flask, request, json, jsonify 
import psycopg2
import jwt
import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = "thisismysecretkey"


def connection():
	connect = psycopg2.connect(
			user = "postgres",
			password = "password",
			host = "localhost",
			port = "5432",
			database = "kasu_logbook_db"
			)
	return connect

def token_reguired(f):
	@wraps(f)

	def decorated(*args, **kwargs):
		Token = request.args.get('token')

		if not Token:
			return {"response": "Token missing"}
		else:
			data = jwt.decode(Token, app.config["SECRET_KEY"], algorithms="HS256")

			return f(*args, **kwargs)
	return decorated

@app.route("/")
@token_reguired
def index():
	return "this is the beginning"

@app.route("/create-user", methods=["POST"])
def create_user():
		conn = connection()
		cursor = conn.cursor()

		if request.method == "POST":
			email = request.json['email']
			password = request.json['password']

			hashed_password = generate_password_hash(password)

			query = "INSERT INTO users(email, password)VALUES(%s, %s)"
			bind = (email, hashed_password)

			cursor.execute(query, bind)
			conn.commit()
			conn.close()

			return {"response": "User added successfully"}

@app.route("/login", methods=["POST"])
def login():
	conn = connection()
	cursor = conn.cursor()

	if request.method == "POST":
		email = request.json['email']
		password = request.json['password']

		query = "SELECT email, password, user_id FROM users WHERE email = %s"
		bind = (email,)

		cursor.execute(query, bind)
		row = cursor.fetchone()
		# print(row)
		
		_email = row[0]
		_password = row[1]


		confirm_password = check_password_hash(_password, password)

		if confirm_password:
			token = jwt.encode({'user': _email, 'exp': datetime.datetime.now() + datetime.timedelta(seconds = 20)}, app.config["SECRET_KEY"], algorithm="HS256")

			return {"token": token}

		else:
			return {"response": "password incorrect please input a valid password"}


@app.route("/student-particulars", methods=["POST"])
@token_reguired
def student_particulars():
	conn = connection()
	cursor = conn.cursor()

	if request.method == "POST":
		name = request.json['name']
		user_id = request.json['user_id']
		department = request.json['department']
		reg_number = request.json['reg_number']
		course_of_study = request.json['course_of_study']
		course_duration = request.json['course_duration']
		phone_number = request.json['phone_number']
		p_g_phoneNumber = request.json['p_g_phoneNumber']
		account_name = request.json['account_name']
		bank_name = request.json['bank_name']
		bank_account_no = request.json['bank_account_no']
		bank_sort_code = request.json['bank_account_no']
		name_of_establishment = request.json['name_of_establishment']
		address_of_establishment = request.json['address_of_establishment']
		period_of_attachment = request.json['period_of_attachment']
		industry_supervisor_name  = request.json['industry_supervisor_name']
		industry_supervisor_phoneNumber = request.json['industry_supervisor_phoneNumber']
		email = request.json['email']
		

		query = """INSERT INTO student_particulars(name, user_id, department, reg_number, email, course_of_study, course_duration, phone_number, 
													pg_phoneNumber, account_name, bank_name, bank_sort_code, bank_account_no, 
													name_of_establishment, address_of_establishment, period_of_attachment, 
													industry_supervisor_name, industry_supervisor_email, industry_supervisor_phoneNumbers)VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
		bind = (name, user_id, department, reg_number, email, course_of_study, 
					course_duration, phone_number, p_g_phoneNumber, 
					account_name, bank_name, bank_sort_code, bank_account_no, name_of_establishment,
					address_of_establishment, period_of_attachment,
					industry_supervisor_name)

		cursor.execute(query, bind)
		conn.commit()
		conn.close()

		return {"response": "Student particulars added successfully"}

@app.route("/get_student_particulars", methods=["POST"])
@token_reguired
def getParticulars():
	conn = connection()
	cursor = conn.cursor()

	student_id =request.json["student_id"]

	query = "SELECT * FROM student_particulars WHERE user_id=%s"
	bind = (student_id,)

	cursor.execute(query, bind)
	rows = cursor.fetchall()
	conn.close()

	student_particulars = []

	for row in rows:
		print(row)
		particulars = {"particular_id": row[0], "user_id": row[1], "name": row[2], "department": row[3], 
						"reg_number": row[4], "course_of_study": row[5], "course_duration": row[6], 
						"phone_number": row[7], "email": row[8], "p_g_phoneNumber":row[9], "account_name": row[10], 
						"bank_name": row[11], "bank_account_no": row[12], "name_of_establishment": row[13], 
						"address_of_establishment": row[14], "period_of_attachment": row[15], 
						"industry_supervisor_name": row[16], "industry_supervisor_email": row[17], 
						"industry_supervisor_phoneNumber": row[18], "updated_particulars": row[19], 
						"bank_sort_code": row[20]

						}
		student_particulars.append(particulars)

	return jsonify(student_particulars)

@app.route("/get_current_user_id",methods=["POST"])
@token_reguired
def getCurrentUser():
	conn = connection()
	cursor = conn.cursor()

	email = request.json['email']

	query = "SELECT user_id FROM users WHERE email = %s"
	bind = (email,)

	cursor.execute(query, bind)
	row = cursor.fetchall()
	print(row)
	conn.close()

	return {"current_user":row[0][0]}


@app.route("/progress-report", methods=["POST"])
@token_reguired
def report():
	conn = connection()
	cursor = conn.cursor()

	user_id = request.json['user_id']
	week_day= request.json['week_day']
	weekending = request.json['weekending_date']
	report = request.json['progress-report']
	student_signature = request.json['student_signature']
	date_submitted = datetime.datetime.now()
	comment_industrial_based_supervisor = request.json['industry_supervisor_comment']
	name_of_industrial_based_supervisor = request.json['industry_supervisor_name']

	query = "INSERT INTO report(user_id, day, report, student_signature, weekending, date_submitted, comment_industrial_based_supervisor, name_of_industrial_based_supervisor)VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
	bind = (user_id, week_day, report, student_signature, weekending, date_submitted, comment_industrial_based_supervisor, name_of_industrial_based_supervisor)

	cursor.execute(query, bind)
	conn.commit()
	conn.close()

	return {"reponse": "report submitted successfully"}


@app.route("/create-school-supervisors", methods=["POST"])
@token_reguired
def school_supervisors():
	conn = connection()
	cursor = conn.cursor()

	name = request.json['name']
	email = request.json['email']
	phone_number = request.json['phone_number']
	department = request.json['department']

	query = """ INSERT INTO supervisor(supervisor_name, supervisor_email, supervisor_phoneNumber, supervisor_department)
				VALUES(%s, %s, %s, %s)"""
	bind = (name, email, phone_number, department)

	cursor.execute(query, bind)
	conn.commit()
	conn.close()

	return {"reponse": "successfully created a supervisor"}


@app.route("/create-industry-supervisor")
@token_reguired
def insutrial_supervisor():
	conn = connection()
	cursor = conn.cursor()

	name = request.json['name']
	email = request.json['email']
	phone = request.json['phoneNumber']

	query = """ INSERT INTO industry_supervisor(supervisor_name, supervisor_email, supervisor_phoneNumber)
				VALUES(%s, %s, %s)"""
	bind = (name, email, phone)

	cursor.execute(query,bind)
	conn.commit()
	conn.close()

	return {"response": "successfully added an industrial based supervisor"}
	





if __name__ == "__main__":
	app.run(debug=True)