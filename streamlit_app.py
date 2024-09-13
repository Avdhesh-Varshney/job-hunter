import streamlit as st
import pandas as pd
import gdown

@st.cache_resource
def load_data():
  gdown.download(f"https://drive.google.com/uc?id={st.secrets['JOB_DATA']}", f'job_data.csv', quiet=False)
  data = pd.read_csv("job_data.csv")
  return data

def generate_company_insights(data):
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

def hr_info(data):
  st.subheader("HR Contact Information")

  hr_names = data["hr_name"].unique()
  selected_hr = st.selectbox("Select a HR", hr_names)
  hr_data = data[data["hr_name"] == selected_hr]
  
  if not hr_data.empty:
    st.write(f"**Name:** {selected_hr}")
    col1, col2 = st.columns(2)
    
    with col1:
      st.write(f"**Job Title:** {hr_data['hr_job_title'].values[0]}")
      st.write(f"**Email:** {hr_data['hr_email'].values[0]}")
      st.write(f"**Phone:** {hr_data['hr_phone'].values[0]}")

    with col2:
      linkedin_url = hr_data['hr_linkedin_username'].values[0]
      twitter_url = hr_data['hr_twitter_username'].values[0]
      facebook_url = hr_data['hr_facebook_username'].values[0]
      
      st.write("**LinkedIn:**", f"[{linkedin_url}](https://www.linkedin.com/in/{linkedin_url})" if pd.notna(linkedin_url) else "N/A")
      st.write("**Twitter:**", f"[{twitter_url}](https://twitter.com/{twitter_url})" if pd.notna(twitter_url) else "N/A")
      st.write("**Facebook:**", f"[{facebook_url}](https://www.facebook.com/{facebook_url})" if pd.notna(facebook_url) else "N/A")
  else:
    st.warning("No data available for the selected HR contact.", icon="⚠️")

def company_info(data):
  st.subheader("About Company and its Contacts")

  company_names = data["company_name"].unique()
  selected_company = st.selectbox("Select a Company", company_names)
  company_data = data[data["company_name"] == selected_company]
  
  if not company_data.empty:
    st.write(f"**Company:** {selected_company}")
    col1, col2 = st.columns(2)
    
    with col1:
      st.write(f"**Company Niche:** {company_data['company_niche'].values[0]}")
      st.write(f"**Location:** {company_data['company_location'].values[0]}")
      st.write(f"**Website:** [{company_data['company_website'].values[0]}]({company_data['company_website'].values[0]})")
      st.write(f"**HR Contact:** {company_data['hr_name'].values[0]}")

    with col2:
      st.write(f"**Email:** {company_data['company_email'].values[0]}")
      st.write(f"**LinkedIn:** [{company_data['company_linkedin_username'].values[0]}](https://www.linkedin.com/company/{company_data['company_linkedin_username'].values[0]})")
      st.write(f"**Twitter:** [{company_data['company_twitter_username'].values[0]}](https://twitter.com/{company_data['company_twitter_username'].values[0]})")
      st.write(f"**Facebook:** [{company_data['company_facebook_username'].values[0]}](https://www.facebook.com/{company_data['company_facebook_username'].values[0]})")

  else:
    st.warning("No data available for the selected company.", icon="⚠️")

def main():
  st.sidebar.title("Job Hunter Pro")
  options = ["Company Insights", "Company Information", "HR Information"]
  choice = st.sidebar.selectbox("Select an option", options)
  data = load_data()

  if choice == "Company Insights":
    st.title("Job Hunter Pro Application")
    st.write("A personalized app designed to help job seekers manage their HR contacts, companies, and interactions across multiple platforms (LinkedIn, Email, Twitter). The app automates the outreach process, tracks communications, and provides follow-up reminders.")
    generate_company_insights(data)

  elif choice == "Company Information":
    company_info(data)

  elif choice == "HR Information":
    hr_info(data)

if __name__ == '__main__':
  main()
