from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    details = db.Column(db.String(200), nullable=True)

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        details = request.form["details"]

        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            message = "⚠️ Username already exists!"
        else:
            new_user = User(username=username, password=password, details=details)
            db.session.add(new_user)
            db.session.commit()
            message = "✅ User registered successfully!"
    
    users = User.query.all()
    return render_template("index.html", message=message, users=users)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
