from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Oracle 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle+cx_oracle://shinnk:1253@shinnk.iptime.org:11521/XE'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

if __name__ == '__main__':
    from views import main_blueprint  # 블루프린트 등록
    app.register_blueprint(main_blueprint)
    
    with app.app_context():
        db.create_all()  # 데이터베이스와 테이블 생성
    app.run(debug=True)
