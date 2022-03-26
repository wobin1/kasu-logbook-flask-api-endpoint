CREATE TABLE users(
	user_id serial PRIMARY KEY,
	email VARCHAR(100),
	password VARCHAR(500)
)

CREATE TABLE student_particulars(
	particular_id serial PRIMARY KEY,
	user_id INT,
	name VARCHAR(50),
	department VARCHAR(50),
	reg_number VARCHAR(50),
	course_of_study VARCHAR(50),
	course_duration VARCHAR(20),
	phone_number VARCHAR(20),
	email VARCHAR(50),
	pg_phoneNumber VARCHAR(20),
	account_name VARCHAR(100),
	bank_name VARCHAR(100),
	bank_account_no VARCHAR(50),
	name_of_establishment VARCHAR(50),
	address_of_establishment VARCHAR(50),
	period_of_attachment VARCHAR(50),
	supervisor_id INT,
	industry_supervisor_phoneNumber VARCHAR(20),

	FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
	FOREIGN KEY (supervisor_id)  REFERENCES supervisor(supervisor_id)
)


CREATE TABLE report(
	report_id serial PRIMARY KEY,
	user_id INT,
	day VARCHAR(50) NOT NUll,
	weekending DATE,
	report VARCHAR(2000),
	student_signature VARCHAR(20),
	date_submitted DATE NOT NULL,
	comment_industrial_based_supervisor VARCHAR(300),
	name_of_industrial_based_supervisor INT,

	FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
	FOREIGN KEY (name_of_industrial_based_supervisor) REFERENCES users(user_id) ON DELETE CASCADE

)


CREATE TABLE supervisor(
	supervisor_id serial PRIMARY KEY,
	supervisor_name VARCHAR(100),
	supervisor_email VARCHAR(100),
	supervisor_phoneNumber VARCHAR(20),
	supervisor_department VARCHAR(100)
)

CREATE TABLE industry_supervisor(
	industry_supervisor_id serial PRIMARY KEY,
	industry_supervisor_name VARCHAR(100),
	industry_supervisor_email VARCHAR(100),
	industry_supervisor_phoneNumber VARCHAR(20),
	student INT

	FOREIGN KEY (student) REFERENCES users(user_id) ON DELETE CASCADE

)

CREATE TABLE registration_code(
	code_id serial PRIMARY KEY,
	code VARCHAR(200)
)

