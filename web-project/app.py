from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# 定义数据库并初始化
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# 定义用户类
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.username}')"

@app.route('/')
def index():
    with app.app_context():
        users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/add', methods=['POST'])
def add_user():
    with app.app_context():
        username = request.form.get('username')
        if username:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
    return index()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

