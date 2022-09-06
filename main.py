from datetime import datetime
import databutton as db
import streamlit as st
import pandas as pd
import streamlit as st
import pandas as pd
import numpy as np
from evaluate import validate_df, score_df

columns = ["Participant", "Submission name", "Timestamp", "Score"]
participants = ["P1", "P2", "P3"]
def get_df():
    df = pd.DataFrame(columns=columns, data=[[p, " This is a description of the submission ", datetime.now(), 0] for p in participants])
    return df

df = get_df()
db.storage.dataframes.put(df, "leaderboard")

@db.apps.streamlit(route="/leaderboard", name="Leaderboard")
def leaderboard():
    st.set_page_config(
     page_title="EDC Leaderboard",
     page_icon="🔮")
    st.title(" EDC AzureML Hackathon 2022 ")
    df = db.storage.dataframes.get("leaderboard")
    placeholder = st.empty()
    with placeholder.container():
        ## Sidebar
        st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/c/c6/Equinor.svg", width=200)
        submitter = st.sidebar.selectbox("Submitter", participants)
        submission_name = st.sidebar.text_input("Submission name")
        uploaded_file = st.sidebar.file_uploader("Upload a CSV file",type="csv")
        button_placeholder = st.sidebar.empty()
        button_placeholder.button("Submit", key="sb", disabled=True)
        if uploaded_file is not None:
                sub = pd.read_csv(uploaded_file)
                valid = validate_df(sub)
                if valid:
                    submit = button_placeholder.button("Submit", key="sb2", disabled=False)
                    if submit:
                        score = score_df(sub)
                        new_row = pd.DataFrame(columns=columns, data=[[submitter, submission_name, datetime.now(), score]])
                        df = df.append(new_row, ignore_index=True)
                        df = df.sort_values(by="Score", ascending=True)
                        df.reset_index(drop=True, inplace=True)
                        db.storage.dataframes.put(df, "leaderboard")
                        st.sidebar.success("Submission successful")
                        st.sidebar.balloons()
                        submit = False
                        uploaded_file = None
                else:
                    st.sidebar.error("Invalid submission. Make sure the dataframe is valid.")
        st.dataframe(df, width=1000)
        #db.streamlit.footer() 
                     
    st.sidebar.info(
            f"""
                👆 Upload a .csv file to make your submission. 
                Must be formatted like this: [sample_submission.csv](https://docs.google.com/spreadsheets/d/1DRI23Ywh_jnjU22hOSXQ-fFY-WF0v6ngpIKHlM3cmzU/export?format=csv)
                """
        )
    
    

@db.jobs.repeat_every(seconds=10 * 60)
def repeating_job():
    # Check for new data
    # Do some work on that data
    # Write that data to db.dataframes
    # Send slack notification
    print("Success!")
