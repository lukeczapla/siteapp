from flask import *
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://uyykvnegbmzifr:fabae99afd7f836bbe4c7f10cadb71b409d2bf5d080c947f602251237c810a9e@ec2-50-17-220-223.compute-1.amazonaws.com:5432/d4j4jtln9ih58i'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
 
@app.route("/")
def hello():
    return render_template('fqaMain.html')

# This would be a POST request and returns JSON
@app.route('/submitSearch', methods=['POST'])
def submitSearch():
    filterData = request.get_json(silent=True)
    print "filterData: ", filterData
    for filter in filterData:
    	if filter['name'] == "filterString":
    		print "filterString = ", filter['value']
    	else:
    		print filter['name']
    	# Here we would search the database and assemble the "real" question table commands
		
	# For this prototype, we will hard code the question area with just 2 questions
	# This returns the dasta to the HTML for dusplay in the table
	questionText = ""
	questionText += "<tr><td>  <input type='radio'> This is a sample question </td></tr>"
	questionText += "<tr><td>  <input type='radio'> This is another question </td></tr>"
	print "questionText = ", questionText

    return jsonify(questions=questionText)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    first_name = db.Column(db.String(64), unique=False, index=True)
    last_name = db.Column(db.String(64), unique=False, index=True)
    role = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password = db.Column(db.String(64), unique=False, index=True)
    def __repr__(self):
      return '<User %r>' % self.email


if __name__ == "__main__":
    app.run()

