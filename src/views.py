from flask import Blueprint, render_template
from models import Department  # 모델 임포트
from models import Employee

from app import db  # db 세션 임포트 (app.py에서 정의된 경우)

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def test():
    # 모든 부서 정보를 가져오기
    departments = Department.query.all()  # 데이터베이스에서 모든 부서 조회
    return render_template('home.html', departments=departments)  # 템플릿에 부서 정보 전달
