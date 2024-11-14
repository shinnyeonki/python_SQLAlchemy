from sqlalchemy import CheckConstraint, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app import db  # Assuming SQLAlchemy is initialized in app.py

class Department(db.Model):
    __tablename__ = 'Department'
    department_id = Column(Integer, primary_key=True)
    department_name = Column(String(50), CheckConstraint("department_name IN ('마케팅', '경영관리', '연구개발', '개발', '인사', '영업', '디자인')"), nullable=False)
    # employees = relationship('Employee', backref='department')


class Employee(db.Model):
    __tablename__ = 'Employee'
    employee_id = Column(Integer, primary_key=True)
    department_id = Column(Integer, ForeignKey('Department.department_id'), nullable=False)
    employee_name = Column(String(30), nullable=False)
    registration_number = Column(String(14), nullable=False)
    education_level = Column(String(50), nullable=False)
    skill_set = Column(String(200))
    employee_email = Column(String(50))
    employee_phone_number = Column(String(20))
    employee_address = Column(String(100))

    # department = relationship('Department', backref='employees')
    contracts = relationship('Contract', backref='employee')
    salaries = relationship('Salary', backref='employee')
    participations = relationship('ParticipationProject', backref='employee')
    peer_evaluations = relationship('PeerEvaluation', foreign_keys='PeerEvaluation.evaluator_id', backref='evaluator')
    peer_evaluations_received = relationship('PeerEvaluation', foreign_keys='PeerEvaluation.evaluated_employee_id', backref='evaluated')
    pm_evaluations = relationship('PMEvaluation', foreign_keys='PMEvaluation.evaluator_id', backref='pm_evaluator')
    pm_evaluations_received = relationship('PMEvaluation', foreign_keys='PMEvaluation.evaluated_employee_id', backref='pm_evaluated')
    customer_evaluations = relationship('CustomerEvaluation', foreign_keys='CustomerEvaluation.evaluator_id', backref='customer_evaluator')
    customer_evaluations_received = relationship('CustomerEvaluation', foreign_keys='CustomerEvaluation.evaluated_employee_id', backref='customer_evaluated')


class Customer(db.Model):
    __tablename__ = 'Customer'
    customer_id = Column(Integer, primary_key=True)
    customer_name = Column(String(30), nullable=False)
    customer_email = Column(String(50))
    customer_phone_number = Column(String(20))
    customer_address = Column(String(100))

    projects = relationship('Project', backref='customer')


class Project(db.Model):
    __tablename__ = 'Project'
    project_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('Customer.customer_id'), nullable=False)
    project_name = Column(String(100), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, CheckConstraint('end_date >= start_date'))

    participations = relationship('ParticipationProject', backref='project')
    peer_evaluations = relationship('PeerEvaluation', backref='project')
    pm_evaluations = relationship('PMEvaluation', backref='project')
    customer_evaluations = relationship('CustomerEvaluation', backref='project')
    incentives = relationship('Incentive', backref='project')


class ParticipationProject(db.Model):
    __tablename__ = 'ParticipationProject'
    employee_id = Column(Integer, ForeignKey('Employee.employee_id'), primary_key=True)
    project_id = Column(Integer, ForeignKey('Project.project_id'), primary_key=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, CheckConstraint('end_date >= start_date'))
    role = Column(String(30), CheckConstraint("role IN ('PM', 'PL', 'Analyst', 'Designer', 'Programmer', 'Tester', 'other')"), nullable=False)


class Contract(db.Model):
    __tablename__ = 'Contract'
    contract_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('Employee.employee_id'), nullable=False)
    annual_salary = Column(Integer, nullable=False)
    contract_date = Column(Date, nullable=False)

    salaries = relationship('Salary', backref='contract')


class Salary(db.Model):
    __tablename__ = 'Salary'
    salary_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('Employee.employee_id'), nullable=False)
    contract_id = Column(Integer, ForeignKey('Contract.contract_id'), nullable=False)
    base_salary = Column(Integer, nullable=False)
    monthly_salary = Column(Integer, nullable=False)
    salary_date = Column(Date, nullable=False)


class PeerEvaluation(db.Model):
    __tablename__ = 'PeerEvaluation'
    evaluation_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('Project.project_id'), nullable=False)
    evaluator_id = Column(Integer, ForeignKey('Employee.employee_id'), nullable=False)
    evaluated_employee_id = Column(Integer, ForeignKey('Employee.employee_id'), nullable=False)
    score = Column(Integer, CheckConstraint('score BETWEEN 0 AND 10'), nullable=False)


class PeerEvaluationType(db.Model):
    __tablename__ = 'PeerEvaluationType'
    evaluation_id = Column(Integer, ForeignKey('PeerEvaluation.evaluation_id'), primary_key=True)
    evaluation_type = Column(String(50), primary_key=True)
    evaluation_content = Column(String(500))


class PMEvaluation(db.Model):
    __tablename__ = 'PMEvaluation'
    evaluation_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('Project.project_id'), nullable=False)
    evaluator_id = Column(Integer, ForeignKey('Employee.employee_id'), nullable=False)
    evaluated_employee_id = Column(Integer, ForeignKey('Employee.employee_id'), nullable=False)
    score = Column(Integer, nullable=False)


class PMEvaluationType(db.Model):
    __tablename__ = 'PMEvaluationType'
    evaluation_id = Column(Integer, ForeignKey('PMEvaluation.evaluation_id'), primary_key=True)
    evaluation_type = Column(String(50), primary_key=True)
    evaluation_content = Column(String(500))


class CustomerEvaluation(db.Model):
    __tablename__ = 'CustomerEvaluation'
    evaluation_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('Project.project_id'), nullable=False)
    evaluator_id = Column(Integer, ForeignKey('Customer.customer_id'), nullable=False)
    evaluated_employee_id = Column(Integer, ForeignKey('Employee.employee_id'), nullable=False)
    score = Column(Integer, nullable=False)


class CustomerEvaluationType(db.Model):
    __tablename__ = 'CustomerEvaluationType'
    evaluation_id = Column(Integer, ForeignKey('CustomerEvaluation.evaluation_id'), primary_key=True)
    evaluation_type = Column(String(50), primary_key=True)
    evaluation_content = Column(String(500))


class Incentive(db.Model):
    __tablename__ = 'Incentive'
    project_id = Column(Integer, ForeignKey('Project.project_id'), primary_key=True)
    employee_id = Column(Integer, ForeignKey('Employee.employee_id'), primary_key=True)
    incentive_amount = Column(Integer, nullable=False)


class Seminar(db.Model):
    __tablename__ = 'Seminar'
    seminar_id = Column(Integer, primary_key=True)
    seminar_name = Column(String(100), nullable=False)
    seminar_date = Column(Date, nullable=False)
    seminar_instructor = Column(String(100), nullable=False)


class SeminarParticipation(db.Model):
    __tablename__ = 'SeminarParticipation'
    seminar_id = Column(Integer, ForeignKey('Seminar.seminar_id'), primary_key=True)
    employee_id = Column(Integer, ForeignKey('Employee.employee_id'), primary_key=True)
