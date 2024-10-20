import streamlit as st
import pandas as pd
import gdown
import time

from main.company_hr_info import company_hr_info
from main.about_company import about_company
from main.my_status import my_status

if 'valid' not in st.session_state:
  st.session_state.valid = False
if 'edit' not in st.session_state:
  st.session_state.edit = True
if 'entered_key' not in st.session_state:
  st.session_state.entered_key = 0
if 'open_ai_api_key' not in st.session_state:
  st.session_state.open_ai_api_key = ""
if 'gemini_api_key' not in st.session_state:
  st.session_state.gemini_api_key = ""

aboutApp = '''
A personalized app designed to help job seekers manage their HR contacts, companies, and interactions across multiple \
  platforms (LinkedIn, Email, Twitter). The app automates the outreach process, tracks communications, and provides \
    follow-up reminders.
'''

@st.cache_resource
def connectingServer():
  gdown.download(f"https://drive.google.com/uc?id={st.secrets['JOB_DATA']}", f'job_data.csv', quiet=False)
  data = pd.read_csv("job_data.csv")
  return data

def startApp(data):
  st.sidebar.title("Job Hunter Pro")
  options = ["Company/HR Contact Information", "Company Information", "My Status"]
  choice = st.sidebar.selectbox("Select an option", options)
  if choice == "Company/HR Contact Information":
    company_hr_info(data)
  elif choice == "Company Information":
    about_company(data)
  elif choice == "My Status":
    if st.session_state.entered_key == st.secrets['SECRET_KEY']:
      my_status(data)
    else:
      st.header("You have not access for this area.")
      st.write("### Contact Admin for Secret Key")
      st.toast("You don't have the access for this area.", icon="🚨")

if __name__ == '__main__':
  data = connectingServer()

  if st.session_state.valid:
    startApp(data)

  else:
    st.title("Job Hunter Pro Application")
    st.write(aboutApp)
    key = st.number_input('Enter a valid password', min_value=1000, max_value=9999, step=1, placeholder=1000)
    if st.button('Start App'):
      st.session_state.entered_key = key
      if key in st.secrets['PASSWORDS']:
        st.session_state.valid = True
        st.toast("Login Successful!", icon="✅")
        st.balloons()
        time.sleep(2)
        st.rerun()
      else:
        st.toast("Invalid Key!", icon="🚨")
