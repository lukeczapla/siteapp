from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required


#from src import *
import urllib
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://uyykvnegbmzifr:fabae99afd7f836bbe4c7f10cadb71b409d2bf5d080c947f602251237c810a9e@ec2-50-17-220-223.compute-1.amazonaws.com:5432/d4j4jtln9ih58i'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "GWC Loreal"
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

msgcount = 0
messages = []
access = {}

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

# this is the home page for the L'Oreal app
@app.route("/")
def hello():
	return render_template('loreal.html')

@app.route("/questions")
def questions():
	return render_template('fqaMain.html')

@app.route("/loginform")
def loginform():
  return render_template('login.html', invalid=False)

@app.route('/signupform')
def signupform():
  return render_template('signup.html')

@app.route('/discover')
def discover():
  return render_template('discover.html')


@app.route('/signup', methods=['POST'])
def signup():
  existingusers = User.query.filter_by(email=request.form['email']).all()
  if len(existingusers) > 0:
  	return "You are already signed up"
  r = Role.query.filter_by(name='User').first()
  newuser = User(first_name=request.form['fname'], last_name=request.form['lname'], email=request.form['email'], password=request.form['password'], role=r.id)
  db.session.add(newuser)
  db.session.commit()
  login_user(newuser)
  return redirect("/")

@app.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect("/")

@app.route('/check', methods=['POST'])
def check():
  lemail = request.form['email']
  result = User.query.filter_by(email=lemail).all()
  if len(result) == 0:
    return "INVALID"
  else:
    return "VALID " + str(result[0].id+1000)

@app.route('/login', methods=['GET','POST'])
def login():
  lemail = request.form['email']
  lpw = request.form['password']
  result = User.query.filter_by(email=lemail,password=lpw).all()
  if len(result) != 0:
    login_user(result[0])
    return redirect('/')
  else:
    return render_template('login.html', invalid=True)



# These are pages displayed when there is an error!
@app.errorhandler(404)
def pagenotfound(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internalservererror(e):
	return render_template('500.html'), 500


# Below are all the classes that define data in the database
# each type is a table with multiple rows and the variables
# are the columns

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	def __repr__(self):
		return '<Role %r>' % self.name

class User(db.Model, UserMixin):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), unique=True, index=True)
	first_name = db.Column(db.String(64), unique=False, index=True)
	last_name = db.Column(db.String(64), unique=False, index=True)
	role = db.Column(db.Integer, db.ForeignKey('roles.id'))
	password = db.Column(db.String(64), unique=False, index=True)
	is_active = True
	def __repr__(self):
	  return '<User %r>' % self.email

class Profile(db.Model):
	__tablename__ = "profiles"
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	def __repr__(self):
		return "<Profile %r" % self.id

class Question(db.Model):
	__tablename__ = 'questions'
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.Text, unique=False)
	user = db.Column(db.Integer, db.ForeignKey('users.id'))
	def __repr__(self):
		return '<Question %r>' % self.text

class Purchase(db.Model):
	__tablename__ = 'purchases'
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, unique=False)
	product = db.Column(db.Integer, db.ForeignKey('products.id'))
	user = db.Column(db.Integer, db.ForeignKey('users.id'))
	def __repr__(self):
		return '<Purchase %r by user %r>' % self.id, self.user

class Promocode(db.Model):
	__tablename__ = 'promocodes'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.Integer, unique=True)
	co2 = db.Column(db.Integer, unique=False)
	water = db.Column(db.Integer, unique=False)
	plastic = db.Column(db.Integer, unique=False)
	points = db.Column(db.Integer, unique=False)
	def __repr__(self):
		return '<Promocode %r>' % self.id

class Product(db.Model):
	__tablename__ = 'products'
	id = db.Column(db.Integer, primary_key=True)
	desc = db.Column(db.Text, unique=False)
	code = db.Column(db.String(64), unique=True)
	def __repr__(self):
		return '<Product %r>' % self.id


if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
    #app.run()
    #app.run(host='0.0.0.0',port='443', ssl_context=context)
    #app.run(host='0.0.0.0',port=80)

