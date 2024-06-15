from sqlalchemy import create_engine, Column, Integer, String,DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship
from datetime import datetime
from io import BytesIO
#import openpyxl

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True, autoincrement=True)
    emcode = Column(String, nullable=False)
    emfname = Column(String, nullable=False)
    emlname = Column(String, nullable=False)
    employee_fathername = Column(String, nullable=False)
    emdob = Column(String, nullable=False)
    emdoj = Column(String, nullable=False)
    emdoc = Column(String, nullable=False)
    embranchpid = Column(String, nullable=False)
    emdepartmentpid = Column(String, nullable=False)
    emdesignationpid = Column(String, nullable=False)
    emgradepid = Column(String, nullable=False)
    empan = Column(String, nullable=False)
    emaadhar = Column(String, nullable=False)
    emuan = Column(String, nullable=False)
    
    #rollouts = relationship('SurveyRollout', back_populates='employees')
    #salary_structures = relationship('SalaryStructure', back_populates='employees')


class SalaryHead(Base):
    __tablename__ = 'salary_heads'
    id = Column(Integer, primary_key=True)
    head_code = Column(String, unique=True)
    head_name = Column(String, unique=True)
    head_description = Column(String)
    calculate_on_weo = Column(Boolean)
    calculate_on_phy = Column(Boolean)
    calculate_on_attendance = Column(Boolean)

class SalaryStructure(Base):
    __tablename__ = 'salary_structures'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    salary_head_id = Column(Integer, ForeignKey('salary_heads.id'))
    value = Column(Integer)
    #employees = relationship('Employee', back_populates='salary_structures')
    #salary_head = relationship('SalaryHead')  

class Branch(Base):
    __tablename__ = 'branches'
    branch_id = Column(Integer, primary_key=True,autoincrement=True)
    branch_code=Column(String,nullable=False)
    branch_name = Column(String)

class Department(Base):
    __tablename__ = 'departments'
    department_id = Column(Integer, primary_key=True,autoincrement=True)
    department_code = Column(String,nullable=False)
    department_name = Column(String)

class Designation(Base):
    __tablename__ = 'designations'
    designation_id = Column(Integer, primary_key=True,autoincrement=True)
    designation_code = Column(String,nullable=False)
    designation_name = Column(String)

class Grade(Base):
    __tablename__ = 'grades'
    grade_id = Column(Integer, primary_key=True,autoincrement=True)
    grade_code = Column(String,nullable=False)
    grade_name = Column(String)

class SurveyTemplate(Base):
    __tablename__ = 'survey_templates'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    form_structure = Column(String, nullable=False)
    
    #rollouts = relationship('SurveyRollout', back_populates='survey_template')

class SurveyRollout(Base):
    __tablename__ = 'survey_rollouts'
    id = Column(Integer, primary_key=True)
    survey_id = Column(Integer, ForeignKey('survey_templates.id'), nullable=False)
    emp_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    date_of_rollout = Column(DateTime, default=datetime.utcnow)
    date_of_submission = Column(DateTime, nullable=True)
    status = Column(Boolean, default=False)
    
    #survey_template = relationship('SurveyTemplate', back_populates='rollouts')
    #employee = relationship('Employee', back_populates='rollouts')
    
def setup_database():
    engine = create_engine('sqlite:///app.db')
    Base.metadata.create_all(engine)
    
    # Insert default user
    Session = sessionmaker(bind=engine)
    session = Session()
    if not session.query(User).filter_by(username='super').first():
        session.add(User(username='super', password='JayShreeRam'))
        session.commit()
    session.close()

if __name__ == '__main__':
    setup_database()