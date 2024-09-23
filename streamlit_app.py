from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
import streamlit as st
import pandas as pd
import gdown
import time

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

@st.cache_resource
def getDriveService():
  gdown.download(f"https://drive.google.com/uc?id={st.secrets['SERVICE_ACCOUNT_FILE']}", 'credentials.json', quiet=False)
  SCOPES = ['https://www.googleapis.com/auth/drive']
  creds = service_account.Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
  service = build('drive', 'v3', credentials=creds)
  return service

def saveData(data, info, new_row):
  index = data.index[(data['hr_name'] == info['hr_name']) & (data['company_name'] == info['company_name'])].tolist()[0]
  data.loc[index] = new_row.iloc[0]
  data.to_csv('job_data.csv', index=False)
  try:
    service = getDriveService()
    media = MediaFileUpload('job_data.csv', mimetype='application/csv', resumable=True)
    request = service.files().update(fileId=st.secrets['JOB_DATA'], media_body=media, body={'mimeType': 'application/csv'})
    response = request.execute()
    st.success("File updated successfully!", icon="✅")
    return response
  except Exception as e:
    st.error(f"An error occurred while uploading: {e}", icon="🚫")
    return None

def analyzeCompanyData(data):
  st.title("Job Hunter Pro Application")

  st.subheader("Top Companies by Count")
  company_count = data["company_name"].value_counts()
  top_companies = company_count.head(10)
  st.bar_chart(top_companies)

  st.subheader("Top Companies by Location")
  company_location = data.groupby("company_location")["company_name"].count().sort_values(ascending=False)
  top_locations = company_location.head(10)
  st.bar_chart(top_locations)

  st.subheader("Top Companies by Niche")
  company_niche = data.groupby("company_niche")["company_name"].count().sort_values(ascending=False)
  top_niches = company_niche.head(10)
  st.bar_chart(top_niches)

def information(data):
  st.subheader("Company/HR Contact Information")
  category = st.radio("Filter data based on:", ['HR', 'Company'])
  if category == 'HR':
    hr_names = sorted(data["hr_name"].astype(str).unique())
    choice = st.selectbox("Select an HR", hr_names)
    raw_data = data[data["hr_name"] == choice]
  else:
    company_names = sorted(data["company_name"].astype(str).unique())
    choice = st.selectbox("Select a Company", company_names)
    raw_data = data[data["company_name"] == choice]
  info = raw_data.iloc[0]

  st.divider()
  name = st.text_input("Name of the HR", value=info['hr_name'], disabled=st.session_state.edit)
  cola, colb = st.columns(2)
  with cola:
    new_job_title = st.text_input("Job Title", value=info['hr_job_title'], disabled=st.session_state.edit)
    new_email = st.text_input("Email ID", value=info['hr_email'], disabled=st.session_state.edit)
    new_phone = st.text_input("Contact No.", value=info['hr_phone'], disabled=st.session_state.edit)
  with colb:
    new_linkedin_username = st.text_input("LinkedIn Username", value=info['hr_linkedin_username'], disabled=st.session_state.edit)
    new_twitter_username = st.text_input("Twitter Username", value=info['hr_twitter_username'], disabled=st.session_state.edit)
    new_facebook_username = st.text_input("Facebook Username", value=info['hr_facebook_username'], disabled=st.session_state.edit)

  st.divider()
  new_company_name = st.text_input("Name of the Company", value=info['company_name'], disabled=st.session_state.edit)
  new_company_niche = st.text_input("Company Niche", value=info['company_niche'], disabled=st.session_state.edit)
  colx, coly = st.columns(2)
  with colx:
    new_company_website = st.text_input("Company Website URL", value=info['company_website'], disabled=st.session_state.edit)
    new_company_email = st.text_input("Company Email", value=info['company_email'], disabled=st.session_state.edit)
    new_company_location = st.text_input("Company Location", value=info['company_location'], disabled=st.session_state.edit)
  with coly:
    new_company_linkedin_username = st.text_input("Company LinkedIn Username", value=info['company_linkedin_username'], disabled=st.session_state.edit)
    new_company_twitter_username = st.text_input("Company Twitter Username", value=info['company_twitter_username'], disabled=st.session_state.edit)
    new_company_facebook_username = st.text_input("Company Facebook Username", value=info['company_facebook_username'], disabled=st.session_state.edit)

  st.divider()
  if st.session_state.edit:
    if info['status'] == 'No Openings': st.info("There is no opening for Job or You've not reach out to them!", icon="ℹ️")
    elif info['status'] == 'Invitation Sent': st.warning("Mail is already sent!", icon="⚠️")
    else: st.success("You are in-talk with this Company/HR!", icon="✅")

    if info['job_status']: st.success("You've already applied for Job/Internship!", icon="✅")
    else: st.error("You've not applied for Job/Intenship!", icon="🚫")

    if info['linkedin_status']: st.success("You've already contacted with HR/Company on LinkedIn!", icon="✅")
    else: st.error("You've not contacted with HR/Company on LinkedIn!", icon="🚫")

    if info['twitter_status']: st.success("You've already contacted with HR/Company on Twitter!", icon="✅")
    else: st.error("You've not contacted with HR/Company on Twitter!", icon="🚫")

    if info['facebook_status']: st.success("You've already contacted with HR/Company on Facebook!", icon="✅")
    else: st.error("You've not contacted with HR/Company on Facebook!", icon="🚫")

    if st.button("Edit Details", key="edit_btn"):
      st.session_state.edit = False
      st.rerun()

  else:
    my_status = st.selectbox("My Status", ['No Openings', 'Invitation Sent', 'In Talks'])
    applied_for_job = st.checkbox("Have you applied for internship or job?")
    my_linkedin_status = st.checkbox("Have you contact HR/Company on LinkedIn?")
    my_twitter_status = st.checkbox("Have you contact HR/Company on Twitter?")
    my_facebook_status = st.checkbox("Have you contact HR/Company on Facebook?")

    secret_key = st.number_input("Enter the secret key", min_value=1000, max_value=9999, step=1, placeholder=1000)
    if st.button("Save Details", key="save_btn"):
      if secret_key == st.secrets['SECRET_KEY']:
        st.session_state.edit = True
        new_row = pd.DataFrame([{
          'hr_name': name, 'hr_job_title': new_job_title, 'hr_email': new_email, 'hr_phone': new_phone,
          'hr_linkedin_username': new_linkedin_username, 'hr_twitter_username': new_twitter_username,
          'hr_facebook_username': new_facebook_username, 'company_name': new_company_name,
          'company_website': new_company_website, 'company_email': new_company_email,
          'company_linkedin_username': new_company_linkedin_username, 'company_twitter_username': new_company_twitter_username,
          'company_facebook_username': new_company_facebook_username, 'company_location': new_company_location,
          'company_niche': new_company_niche, 'status': my_status, 'job_status': applied_for_job, 
          'linkedin_status': my_linkedin_status, 'twitter_status': my_twitter_status, 'facebook_status': my_facebook_status
        }])
        st.toast("Form Submitted Successfully.", icon="✅")
        time.sleep(1)
        response = saveData(data, info, new_row)
        if response is not None:
          st.toast("Data Saved Successfully!", icon="✅")
        else:
          st.toast("Data is not Saved!", icon="🚨")
        time.sleep(2)
        st.rerun()
      else:
        st.toast("Invalid Key!", icon="🚨")

def myStatus(data):
  st.subheader("My Status")
  data_display = data[['hr_name', 'company_name', 'status', 'job_status', 'linkedin_status', 'twitter_status', 'facebook_status']].copy()
  
  data_display['job_status'] = data_display['job_status'].apply(lambda x: 'Applied' if x else 'Not Applied')
  data_display['linkedin_status'] = data_display['linkedin_status'].apply(lambda x: 'Reached Out' if x else 'Not Reached Out')
  data_display['twitter_status'] = data_display['twitter_status'].apply(lambda x: 'Reached Out' if x else 'Not Reached Out')
  data_display['facebook_status'] = data_display['facebook_status'].apply(lambda x: 'Reached Out' if x else 'Not Reached Out')
  
  status_color_map = {
    'No Openings': '🔴 No Openings',
    'Invitation Sent': '🟡 Invitation Sent',
    'In Talks': '🟢 In Talks'
  }
  data_display['status'] = data_display['status'].map(status_color_map)


  cols = st.columns(2)
  with cols[0]:
    filter_status = st.radio("Filter by Company Status", ['All', 'No Openings', 'Invitation Sent', 'In Talks'])
    if filter_status != 'All':
      data_display = data_display[data_display['status'] == status_color_map[filter_status]]
  with cols[1]:
    filter_job_status = st.checkbox("Filter by Job Status")
    if filter_job_status:
      data_display = data_display[data_display['job_status'] == 'Applied']
    filter_linkedin_status = st.checkbox("Filter by LinkedIn Status")
    if filter_linkedin_status:
      data_display = data_display[data_display['linkedin_status'] == 'Reached Out']
    filter_twitter_status = st.checkbox("Filter by Twitter Status")
    if filter_twitter_status:
      data_display = data_display[data_display['twitter_status'] == 'Reached Out']
    filter_facebook_status = st.checkbox("Filter by Facebook Status")
    if filter_facebook_status:
      data_display = data_display[data_display['facebook_status'] == 'Reached Out']

  unique_names = sorted(data_display['hr_name'].astype(str).unique().tolist() + data_display['company_name'].astype(str).unique().tolist())
  search_term = st.selectbox("Search for Company or HR", ["Select"] + unique_names)
  if search_term != "Select":
    data_display = data_display[data_display.apply(lambda row: (isinstance(row['company_name'], str) and \
                                                                search_term in row['company_name']) or \
                                                                  (isinstance(row['hr_name'], str) and \
                                                                   search_term in row['hr_name']), axis=1)]

  items_per_page = st.slider("No. of Items per page", min_value=1, max_value=20, step=1, value=1)
  total_items = len(data_display)
  total_pages = (total_items // items_per_page) + 1

  if total_pages > 1:
    page = st.slider("Select Page", min_value=1, max_value=total_pages, step=1, value=1)
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page

    st.dataframe(data_display[['hr_name', 'company_name']].iloc[start_idx:end_idx])
    st.write(f"#### Summary of Status")
    status_value_counts = data_display['status'].value_counts()
    st.bar_chart(status_value_counts)
  else:
    st.toast("No Data Found!", icon="🚨")
    st.error("No Data Found!", icon="🚨")

def startApp(data):
  st.sidebar.title("Job Hunter Pro")
  options = ["Company/HR Information", "My Status", "Company Insights"]
  choice = st.sidebar.selectbox("Select an option", options)
  if choice == "Company/HR Information":
    information(data)
  elif choice == "My Status":
    myStatus(data)
  elif choice == "Company Insights":
    analyzeCompanyData(data)

if __name__ == '__main__':
  if 'valid' not in st.session_state:
    st.session_state.valid = False
  if 'edit' not in st.session_state:
    st.session_state.edit = True

  data = connectingServer()
  if st.session_state.valid:
    startApp(data)
  else:
    st.title("Job Hunter Pro Application")
    st.write(aboutApp)
    key = st.number_input('Enter a valid password', min_value=1000, max_value=9999, step=1, placeholder=1000)
    if st.button('Start App'):
      if key in st.secrets['PASSWORDS']:
        st.session_state.valid = True
        st.toast("Login Successful!", icon="✅")
        st.balloons()
        time.sleep(2)
        st.rerun()
      else:
        st.toast("Invalid Key!", icon="🚨")
