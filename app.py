from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SECRET_KEY'] = 'supersecretkey'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form['content']
        if not content.strip():
            flash("Task cannot be empty.", "danger")
            return redirect(url_for('index'))
        new_task = Task(content=content)
        db.session.add(new_task)
        db.session.commit()
        flash("Task added successfully!", "success")
        return redirect('/')
    tasks = Task.query.order_by(Task.date_created.desc()).all()
    return render_template('index.html', tasks=tasks)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        content = request.form['content']
        if not content.strip():
            flash("Task cannot be empty.", "danger")
            return redirect(url_for('edit', id=id))
        task.content = content
        db.session.commit()
        flash("Task updated!", "info")
        return redirect('/')
    return render_template('edit.html', task=task)

@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted.", "warning")
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)