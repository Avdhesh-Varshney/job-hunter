import google.generativeai as genai
from openai import OpenAI
import streamlit as st

def create_prompt(company, website, linkedin, twitter, facebook, location, niche):
    prompt = f"Can you provide a comprehensive overview of {company} that includes the following information:\n\n"
    prompt += "### Major Points\n"
    prompt += "1. **Company Overview**\n"
    prompt += "   - Mission and vision statements\n"
    prompt += "   - Core values and culture\n"
    prompt += "   - Company history and milestones\n\n"

    prompt += "2. **Products and Services**\n"
    prompt += "   - Key products or services offered\n"
    prompt += "   - Unique selling propositions (USPs)\n"
    prompt += "   - Recent launches or innovations\n\n"

    prompt += "3. **Market Position**\n"
    prompt += "   - Industry standing (leaders, competitors)\n"
    prompt += "   - Target audience and customer demographics\n"
    prompt += "   - Market trends and challenges\n\n"

    prompt += "4. **Financial Health**\n"
    prompt += "   - Recent funding rounds or investments\n"
    prompt += "   - Revenue growth and profitability\n"
    prompt += "   - Key financial metrics\n\n"

    prompt += "5. **Work Culture**\n"
    prompt += "   - Employee reviews\n"
    prompt += "   - Work-life balance and remote work policies\n"
    prompt += "   - Diversity and inclusion initiatives\n\n"

    prompt += "6. **Career Opportunities**\n"
    prompt += "   - Current job openings and roles\n"
    prompt += "   - Typical career progression paths\n"
    prompt += "   - Professional development opportunities\n\n"

    prompt += "7. **Leadership Team**\n"
    prompt += "   - Key executives and their backgrounds\n"
    prompt += "   - Leadership style and management approach\n\n"

    prompt += "### Minor Points\n"
    prompt += "1. **Company News**\n"
    prompt += "   - Recent press releases or news articles\n"
    prompt += "   - Awards and recognitions\n"
    prompt += "   - Community involvement and social responsibility efforts\n\n"

    prompt += "2. **Networking Opportunities**\n"
    prompt += "   - Key employees to connect with on LinkedIn\n"
    prompt += "   - Relevant industry events or webinars\n\n"

    prompt += "3. **Tech Stack and Tools**\n"
    prompt += "   - Technologies used in operations\n"
    prompt += "   - Tools for project management and collaboration\n\n"

    prompt += "4. **Work Environment**\n"
    prompt += "   - Office layout and team dynamics\n"
    prompt += "   - Employee engagement activities\n\n"

    prompt += "5. **Interview Process**\n"
    prompt += "   - Typical interview format and common questions\n\n"

    prompt += "6. **Compensation and Benefits**\n"
    prompt += "   - Salary ranges for specific roles\n"
    prompt += "   - Benefits offered\n\n"

    prompt += "7. **Company Policies**\n"
    prompt += "   - Code of conduct and ethical guidelines\n"
    prompt += "   - Policies on promotions and performance reviews\n\n"

    prompt += "### Additional Information\n"
    prompt += f"- **Website**: {website}\n"
    prompt += f"- **LinkedIn**: {linkedin}\n"
    prompt += f"- **Twitter**: {twitter}\n"
    prompt += f"- **Facebook**: {facebook}\n"
    prompt += f"- **Location**: {location}\n"
    prompt += f"- **Niche**: {niche}\n"
    return prompt

def open_ai_response(prompt):
    client = OpenAI(api_key=st.session_state.open_ai_api_key)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        if "Rate limit" in str(e):
            st.error("You have exceeded your API usage limit. Please try again later.", icon="🚨")
        elif "Invalid request" in str(e):
            st.error("Invalid request: Please check your input.", icon="🚨")
        elif "Authentication" in str(e):
            st.error("Authentication error. Please check your API key.", icon="🚨")
        else:
            st.error(f"An unexpected error occurred: {str(e)}", icon="🚨")

def gemini_response(prompt):
    genai.configure(api_key=st.session_state.gemini_api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        if "Rate limit" in str(e):
            st.error("You have exceeded your API usage limit. Please try again later.", icon="🚨")
        elif "Invalid request" in str(e):
            st.error("Invalid request: Please check your input.", icon="🚨")
        elif "Authentication" in str(e):
            st.error("Authentication error. Please check your API key.", icon="🚨")
        else:
            st.error(f"An unexpected error occurred: {str(e)}", icon="🚨")

def get_company_info(company, selected_company_data):
    website = selected_company_data['company_website'].values[0]
    linkedin = selected_company_data['company_linkedin_username'].values[0]
    twitter = selected_company_data['company_twitter_username'].values[0]
    facebook = selected_company_data['company_facebook_username'].values[0]
    location = selected_company_data['company_location'].values[0]
    niche = selected_company_data['company_niche'].values[0]

    prompt_provided = st.expander("Prompt Provided", expanded=False)
    with prompt_provided:
        prompt = create_prompt(company, website, linkedin, twitter, facebook, location, niche)
        st.write(prompt)

    if st.button("Get OpenAI Response"):
        openai_expander = st.expander("OpenAI Response", expanded=False)
        with openai_expander:
            response = open_ai_response(prompt)
            if response is not None:
                st.write(response)

    if st.button("Get Gemini Response"):
        gemini_expander = st.expander("Gemini Response", expanded=False)
        with gemini_expander:
            response = gemini_response(prompt)
            if response is not None:
                st.write(response)

def about_company(data):
    st.title("Job Hunter Pro Application")
    data = data[data['company_name'].notnull()]
    data = data.drop_duplicates(subset='company_name')
    company_cols = ['company_name', 'company_website', 'company_linkedin_username', 'company_twitter_username', 'company_facebook_username', 'company_location', 'company_niche']
    company_data = data[company_cols]

    if st.session_state.get("open_ai_api_key") == "":
        if st.secrets.get('OPEN_AI_API_KEY', "") == "":
            api_key = st.text_input("Enter your own OPEN AI API KEY", type='password')
            if st.button("Enter") and api_key != "":
                st.session_state.open_ai_api_key = api_key
                st.rerun()
        else:
            st.session_state.open_ai_api_key = st.secrets['OPEN_AI_API_KEY']

    if st.session_state.get("gemini_api_key") == "":
        if st.secrets.get('GEMINI_API_KEY', "") == "":
            gemini_key = st.text_input("Enter your own GEMINI API KEY", type='password')
            if st.button("Enter") and gemini_key != "":
                st.session_state.gemini_api_key = gemini_key
                st.rerun()
        else:
            st.session_state.gemini_api_key = st.secrets['GEMINI_API_KEY']

    company = st.selectbox("Know about any company", company_data['company_name'])
    selected_company_data = company_data[company_data['company_name'] == company]
    if st.session_state.entered_key == st.secrets['SECRET_KEY']:
        get_company_info(company, selected_company_data)
    else:
        st.write("### You required the secret key to access this functionality.")
