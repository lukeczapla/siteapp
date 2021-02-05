
from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required


#from src import *
import urllib
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://HIDDEN_DATA'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "GWC Loreal"
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@app.route("/")
def hello():
	return render_template('QandA.html')


@app.route("/loginform")
def loginform():
  return render_template('login.html', invalid=False)

@app.route('/login', methods=['GET','POST'])
def login():
  lemail = request.form['email']
  lpw = request.form['password']
  result = User.query.filter_by(email=lemail,password=lpw).all()
  if len(result) != 0:
    login_user(result[0])
    return render_template('loreal.html')
  else:
    return render_template('login.html', invalid=True)


@app.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect("/")


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


if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
	
