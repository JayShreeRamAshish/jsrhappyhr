import os
import streamlit as st
import smtplib
from setup_db import User, Employee, Base,SurveyTemplate,SurveyRollout,engine
from sqlalchemy import create_engine,inspect,Column,Integer,String,DateTime,Boolean,ForeignKey
from sqlalchemy.orm import sessionmaker,relationship, declarative_base


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def send_email(to_address, subject, body):
    from_address = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")

    message = f"""\
    Subject: {subject}
    To: {to_address}
    From: {from_address}

    {body}
    """

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_address, password)
            server.sendmail(from_address, to_address, message)
    except Exception as e:
        st.error(f"Failed to send email: {e}")

def create_survey_template():
    session = Session()
    st.title("Create Survey Template")
    survey_name = st.text_input("Survey Name")
    
    if 'form_fields' not in st.session_state:
        st.session_state['form_fields'] = []

    field_type = st.selectbox("Select Field Type", ["Text Input", "Date Input", "Number Input"])
    if st.button("Add Field"):
        st.session_state['form_fields'].append(field_type)

    for idx, field in enumerate(st.session_state['form_fields']):
        st.write(f"Field {idx + 1}: {field}")

    if st.button("Save Template"):
        form_structure = json.dumps(st.session_state['form_fields'])
        session = Session()
        new_template = SurveyTemplate(name=survey_name, form_structure=form_structure)
        session.add(new_template)
        session.commit()
        st.success("Survey Template Saved")
        st.session_state['form_fields'] = []  # Reset form fields after saving

def rollout_survey():
    session = Session()
    templates = session.query(SurveyTemplate).all()
    employees = session.query(Employee).all()
    
    template_options = {template.name: template.id for template in templates}
    employee_options = {f"{employee.name} ({employee.emp_code})": employee.id for employee in employees}

    selected_template = st.selectbox("Select Survey Template", list(template_options.keys()))
    selected_employees = st.multiselect("Select employees", list(employee_options.keys()))

    if st.button("Rollout Survey"):
        template_id = template_options[selected_template]
        for emp in selected_employees:
            emp_id = employee_options[emp]
            new_rollout = SurveyRollout(survey_id=template_id, emp_id=emp_id)
            session.add(new_rollout)
            
            # Send survey link email
            employee = session.query(employee).filter(employee.id == emp_id).first()
            survey_link = f"http://example.com/survey?rollout_id={new_rollout.id}"
            email_body = f"Dear {employee.name},\n\nYou have been invited to participate in a survey. Please click the link below to complete the survey:\n{survey_link}\n\nThank you."
            send_email(employee.email, "Survey Invitation", email_body)
            
        session.commit()
        st.success("Survey Rolled Out")

def survey_results():
    session = Session()
    rollouts = session.query(SurveyRollout).all()
    results = []
    
    for rollout in rollouts:
        result = {
            "Employee Code": rollout.employee.emp_code,
            "Employee Name": rollout.employee.name,
            "Date of Rollout": rollout.date_of_rollout,
            "Date of Submission": rollout.date_of_submission,
            "Status": "Submitted" if rollout.status else "Pending"
        }
        results.append(result)
    
    df = pd.DataFrame(results)
    st.dataframe(df)
    
    if st.button("Download Report as PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        for result in results:
            for key, value in result.items():
                pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
            pdf.cell(200, 10, txt=" ", ln=True)  # Add a blank line between entries
        
        pdf_file = "survey_report.pdf"
        pdf.output(pdf_file)
        with open(pdf_file, "rb") as f:
            st.download_button("Download PDF", f, file_name=pdf_file)
