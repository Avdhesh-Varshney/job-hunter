import streamlit as st

def my_status(data):
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
