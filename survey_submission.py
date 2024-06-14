import streamlit as st
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
from setup_db import SurveyRollout
import json
# Database connection
engine = create_engine('sqlite:///survey.db')
Session = sessionmaker(bind=engine)

def submit_survey(rollout_id):
    session = Session()
    rollout = session.query(SurveyRollout).filter(SurveyRollout.id == rollout_id).first()
    
    if rollout and not rollout.status:
        st.title(f"Survey for {rollout.employee.name}")
        form_structure = json.loads(rollout.survey_template.form_structure)
        
        responses = {}
        for idx, field in enumerate(form_structure):
            if field == "Text Input":
                responses[f"field_{idx}"] = st.text_input(f"Field {idx + 1}")
            elif field == "Date Input":
                responses[f"field_{idx}"] = st.date_input(f"Field {idx + 1}")
            elif field == "Number Input":
                responses[f"field_{idx}"] = st.number_input(f"Field {idx + 1}", step=1)
        
        if st.button("Submit Survey"):
            rollout.date_of_submission = datetime.utcnow()
            rollout.status = True
            session.commit()
            st.success("Survey Submitted")
    else:
        st.error("Invalid or already submitted survey")

def main():
    rollout_id = st.experimental_get_query_params().get("rollout_id")
    if rollout_id:
        submit_survey(int(rollout_id[0]))
    else:
        st.error("No survey selected")

if __name__ == '__main__':
    main()
