import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from setup_db import User, Employee, Base
import pandas as pd
from io import BytesIO
import xlsxwriter
from fpdf import FPDF

st.markdown('<style>{}</style>'.format(open('style.css').read()), unsafe_allow_html=True)

# Create an engine
engine = create_engine('sqlite:///app.db')
Session = sessionmaker(bind=engine)

# User management
class UserManagement:
    def __init__(self, session):
        self.session = session

    def create_user(self, username, password):
        new_user = User(username=username, password=password)
        self.session.add(new_user)
        self.session.commit()
        
    def get_employee_by_id(self, emp_id):
        return self.session.query(Employee).filter_by(id=emp_id).first()

    def view_users(self):
        return self.session.query(User).all()
    
    def download_employees_as_excel(self):
        employees = self.view_employees()
        df = pd.DataFrame([(emp.id, emp.emcode, emp.emfname, emp.emlname, emp.employee_fathername,
                            emp.emdob, emp.emdoj, emp.emdoc, emp.embranchpid, emp.emdepartmentpid,
                            emp.emdesignationpid, emp.emgradepid, emp.empan, emp.emaadhar, emp.emuan)
                           for emp in employees],
                          columns=['ID', 'Employee Code', 'First Name', 'Last Name', 'Father Name',
                                   'DOB', 'DOJ', 'DOC', 'Branch', 'Department', 'Designation', 'Grade', 'PAN', 'Aadhar', 'UAN']) 
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Employees')
            writer.save()
        processed_data = output.getvalue()
        return processed_data

    def download_employees_as_pdf(self):
        employees = self.view_employees()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for emp in employees:
            pdf.cell(200, 10, txt=f"ID: {emp.id}, Code: {emp.emcode}, Name: {emp.emfname} {emp.emlname}, Father: {emp.employee_fathername}, DOB: {emp.emdob}, DOJ: {emp.emdoj}, DOC: {emp.emdoc}, Branch: {emp.embranchpid}, Dept: {emp.emdepartmentpid}, Designation: {emp.emdesignationpid}, Grade: {emp.emgradepid}, PAN: {emp.empan}, Aadhar: {emp.emaadhar}, UAN: {emp.emuan}", ln=True)
        return pdf.output(dest='S').encode('latin1')
    

    def modify_user(self, user_id, username, password):
        user = self.session.query(User).filter_by(id=user_id).first()
        user.username = username
        user.password = password
        self.session.commit()

# Employee Central
class EmployeeManagement:
    def __init__(self, session):
        self.session = session

    def create_employee(self,emcode,emfname,emlname,employee_fathername,emdob,emdoj,emdoc,embranchpid,emdepartmentpid,emdesignationpid,emgradepid,empan,emaadhar,emuan):
        new_employee = Employee(
            emcode = emcode,
            emfname = emfname,
            emlname = emlname,
            employee_fathername = employee_fathername,
            emdob = emdob,
            emdoj = emdoj,
            emdoc = emdoc,
            embranchpid = embranchpid,
            emdepartmentpid = emdepartmentpid,
            emdesignationpid = emdesignationpid,
            emgradepid = emgradepid,
            empan = empan,
            emaadhar = emaadhar,
            emuan = emuan)
        self.session.add(new_employee)
        self.session.commit()

    def view_employees(self):
        return self.session.query(Employee).all()
    
    def get_employee_by_id(self, emp_id):
        return self.session.query(Employee).filter_by(id=emp_id).first()
    
    def modify_employee(self, emp_id, emcode, emfname, emlname, employee_fathername, emdob, emdoj, emdoc, embranchpid, emdepartmentpid, emdesignationpid, emgradepid, empan, emaadhar, emuan):
        employee = self.session.query(Employee).filter_by(id=emp_id).first()
        employee.emcode = emcode
        employee.emfname = emfname
        employee.emlname = emlname
        employee.employee_fathername = employee_fathername
        employee.emdob = emdob
        employee.emdoj = emdoj
        employee.emdoc = emdoc
        employee.embranchpid = embranchpid
        employee.emdepartmentpid = emdepartmentpid
        employee.emdesignationpid = emdesignationpid
        employee.emgradepid = emgradepid
        employee.empan = empan
        employee.emaadhar = emaadhar
        employee.emuan = emuan
        self.session.commit()
        
    def download_employees_as_excel(self):
        employees = self.view_employees()
        df = pd.DataFrame([(emp.id, emp.emcode, emp.emfname, emp.emlname, emp.employee_fathername,
                            emp.emdob, emp.emdoj, emp.emdoc, emp.embranchpid, emp.emdepartmentpid,
                            emp.emdesignationpid, emp.emgradepid, emp.empan, emp.emaadhar, emp.emuan)
                           for emp in employees],
                          columns=['ID', 'Employee Code', 'First Name', 'Last Name', 'Father Name',
                                   'DOB', 'DOJ', 'DOC', 'Branch', 'Department', 'Designation', 'Grade', 'PAN', 'Aadhar', 'UAN'])
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Employees')
        writer.save()
        processed_data = output.getvalue()
        return processed_data

    def download_employees_as_pdf(self):
        employees = self.view_employees()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for emp in employees:
            pdf.cell(200, 10, txt=f"ID: {emp.id}, Code: {emp.emcode}, Name: {emp.emfname} {emp.emlname}, Father: {emp.employee_fathername}, DOB: {emp.emdob}, DOJ: {emp.emdoj}, DOC: {emp.emdoc}, Branch: {emp.embranchpid}, Dept: {emp.emdepartmentpid}, Designation: {emp.emdesignationpid}, Grade: {emp.emgradepid}, PAN: {emp.empan}, Aadhar: {emp.emaadhar}, UAN: {emp.emuan}", ln=True)
        return pdf.output(dest='S').encode('latin1')
    

# Login authentication
def login(session, username, password):
    return session.query(User).filter_by(username=username, password=password).first()

# Main Streamlit application
def main():

    # Authentication
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.sidebar.header("Happy-HR")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            session = Session()
            user = login(session, username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Logged in successfully")
            else:
                st.error("Invalid username or password")
            session.close()
        return

    st.sidebar.header("Happy-HR")
    
    menu=st.sidebar.selectbox("HappyHR",["Dashboard","Employee Central","Attendance","Payroll","Recruitment","PMS","eLearning","Data Central","Manage Users"])

    session = Session()
    
    if menu=="Employee Central":
        st.title("Employee Database")
        sub_menu = st.sidebar.selectbox("Select Submenu", ["New Employee","View Employee","Modify Employee"])
        emp_mgmt = EmployeeManagement(session)

        if sub_menu == "New Employee":
            emcode = st.text_input("Employee Code")
            role = st.text_input("Role")
            emfname = st.text_input("First Name")
            emlname = st.text_input("Last Name")
            employee_fathername = st.text_input("Father Name")
            emdob = st.text_input("Date of Birth")
            emdoj = st.text_input("Date of Joining")
            emdoc = st.text_input("Date of Confirmation")
            embranchpid = st.text_input("Branch")
            emdepartmentpid = st.text_input("Department")
            emdesignationpid = st.text_input("Designation")
            emgradepid = st.text_input("Grade")
            empan = st.text_input("PAN")
            emaadhar = st.text_input("Aadhar")
            emuan = st.text_input("PF UAN")            
            if st.button("Create Employee"):
                emp_mgmt.create_employee(emcode,emfname,emlname,employee_fathername,emdob,emdoj,emdoc,embranchpid,emdepartmentpid,emdesignationpid,emgradepid,empan,emaadhar,emuan)
                st.success("Employee created successfully")
                
        elif sub_menu=="View Employee":
            emp_mgmt = EmployeeManagement(session)
            st.title("Employee Database")
            st.subheader("View Employees")
            employees = emp_mgmt.view_employees()
            data = [{
            "ID": emp.id,
            "Employee Code": emp.emcode,
            "First Name": emp.emfname,
            "Last Name": emp.emlname,
            "Father Name": emp.employee_fathername,
            "DOB": emp.emdob,
            "DOJ": emp.emdoj,
            "DOC": emp.emdoc,
            "Branch": emp.embranchpid,
            "Department": emp.emdepartmentpid,
            "Designation": emp.emdesignationpid,
            "Grade": emp.emgradepid,
            "PAN": emp.empan,
            "Aadhar": emp.emaadhar,
            "UAN": emp.emuan,
            } for emp in employees]
            df = pd.DataFrame(data)
            st.dataframe(df,use_container_width=False,hide_index=True)

            st.subheader("Download Employees Data")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Download as Excel"):
                    excel_data = emp_mgmt.download_employees_as_excel()
                    st.download_button(
                    label="Download Excel file",
                    data=excel_data,
                    file_name='employees.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

            with col2:
                if st.button("Download as PDF"):
                    pdf_data = emp_mgmt.download_employees_as_pdf()
                    st.download_button(
                    label="Download PDF file",
                    data=pdf_data,
                    file_name='employees.pdf',
                    mime='application/pdf')
                    session.close()
    
        elif sub_menu == "Modify Employee":
            emp_id = st.number_input("Employee ID", min_value=1, step=1)
            if st.button("Load Employee"):
                employee = emp_mgmt.get_employee_by_id(emp_id)
                if employee:
                    emcode = st.text_input("Employee Code", value=employee.emcode)
                    emfname = st.text_input("First Name", value=employee.emfname)
                    emlname = st.text_input("Last Name", value=employee.emlname)
                    employee_fathername = st.text_input("Father Name", value=employee.employee_fathername)
                    emdob = st.text_input("Date of Birth", value=employee.emdob)
                    emdoj = st.text_input("Date of Joining", value=employee.emdoj)
                    emdoc = st.text_input("Date of Confirmation", value=employee.emdoc)
                    embranchpid = st.text_input("Branch", value=employee.embranchpid)
                    emdepartmentpid = st.text_input("Department", value=employee.emdepartmentpid)
                    emdesignationpid = st.text_input("Designation", value=employee.emdesignationpid)
                    emgradepid = st.text_input("Grade", value=employee.emgradepid)
                    empan = st.text_input("PAN", value=employee.empan)
                    emaadhar = st.text_input("Aadhar", value=employee.emaadhar)
                    emuan = st.text_input("PF UAN", value=employee.emuan)
                    
                    if st.button("Modify Employee"):
                        emp_mgmt.modify_employee(emp_id,emcode,emfname,emlname,employee_fathername,emdob,emdoj,emdoc,embranchpid, emdepartmentpid, emdesignationpid,emgradepid,empan,emaadhar,emuan)
                        st.success("Employee modified successfully")
                    else:
                        st.error("Employee not found")
        
    elif menu == "Manage Users":
        st.subheader("User Management")
        sub_menu = st.sidebar.selectbox("Select Submenu", ["Create User", "View Users", "Modify User"])
        user_mgmt = UserManagement(session)
        if sub_menu == "Create User":
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            if st.button("Create User"):
                    user_mgmt.create_user(username, password)
                    st.success("User created successfully")

        elif sub_menu == "View Users":
                users = user_mgmt.view_users()
                st.write(users)

        elif sub_menu == "Modify User":
                user_id = st.number_input("User ID", min_value=1)
                username = st.text_input("New Username")
                password = st.text_input("New Password", type="password")
                if st.button("Modify User"):
                    user_mgmt.modify_user(user_id, username, password)
                    st.success("User modified successfully")
    
    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.success("Logged out successfully")

    session.close()

if __name__ == '__main__':
    main()