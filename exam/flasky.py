from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///to_do.db'
db = SQLAlchemy(app)

class ToDo(db.Model):
    idx = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return "<Task %r>" % self.idx

@app.route('/', methods=["GET"])
def index():
    tasks = ToDo.query.order_by(ToDo.content.desc()).filter((ToDo.content=='Kevin') | (ToDo.content=='Lea'))
    return render_template("index.html", tasks=tasks)

if __name__ == "__main__":
    db.create_all()
    db.session.query(ToDo).delete()
    todo1 = ToDo()
    todo1.content = "Andi"

    todo2 = ToDo()
    todo2.content = "Lea"

    todo3 = ToDo()
    todo3.content = "Kevin"

    todo4 = ToDo()
    todo4.content = "Flo"
    
    db.session.add(todo1)
    db.session.add(todo2)
    db.session.add(todo3)
    db.session.add(todo4)
    db.session.commit()
    app.run()

