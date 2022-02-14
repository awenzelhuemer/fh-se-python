from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///to_do.db'
db = SQLAlchemy(app)


class ToDo(db.Model):
    idx = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return "<Task %r>" % self.idx


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = ToDo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your new task'
    else:
        tasks = ToDo.query.order_by(ToDo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:idx>')
def delete(idx):
    task_to_delete = ToDo.query.get_or_404(idx)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deleting your task'


@app.route('/update/<int:idx>', methods=['GET', 'POST'])
def update(idx):
    task_to_update = ToDo.query.get_or_404(idx)
    if request.method == 'POST':
        content = request.form['content']
        task_to_update.content = content
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        task_to_update = ToDo.query.get_or_404(idx)
        return render_template('update.html', task=task_to_update)


if __name__ == '__main__':
    app.run()
