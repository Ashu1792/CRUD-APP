from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Employee.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ------------------ MODEL ------------------
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)


# ------------------ HOME (READ) ------------------
@app.route("/")
def home():
    allemployees = Employee.query.all()
    return render_template("index.html", allemployees=allemployees)


# ------------------ ADD EMPLOYEE (CREATE) ------------------
@app.route("/add", methods=["POST"])
def add_employee():
    name = request.form["name"]
    email = request.form["email"]

    new_emp = Employee(name=name, email=email)
    db.session.add(new_emp)
    db.session.commit()

    return redirect(url_for("home"))


# ------------------ ABOUT ------------------
@app.route("/about")
def about():
    return render_template("about.html")
# ------------------ Delete ------------------

@app.route("/delete/<int:id>")
def delete(id):
    emp = Employee.query.get_or_404(id)
    db.session.delete(emp)
    db.session.commit()
    return redirect(url_for("home"))
#------------------Update------------------


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    emp = Employee.query.get_or_404(id)

    if request.method == "POST":
        emp.name = request.form["name"]
        emp.email = request.form["email"]
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("update.html", emp=emp)





if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

