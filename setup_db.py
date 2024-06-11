from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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