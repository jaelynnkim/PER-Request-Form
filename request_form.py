import streamlit as st
from simple_salesforce import Salesforce, SalesforceLogin
import os

# Set the page title and icon - This should be placed at the top
st.set_page_config(page_title="Request Form", page_icon="📝")

# Salesforce credentials from environment variables
SF_USERNAME = os.getenv("SF_USERNAME")  # No default value; ensure environment variable is set
SF_PASSWORD = os.getenv("SF_PASSWORD")
SF_SECURITY_TOKEN = os.getenv("SF_SECURITY_TOKEN")
SF_DOMAIN = 'test'  # Use 'test' if connecting to a Salesforce sandbox

# Connect to Salesforce
try:
    # Attempt to log in to Salesforce using credentials from environment variables
    session_id, instance = SalesforceLogin(
        username=SF_USERNAME, 
        password=SF_PASSWORD, 
        security_token=SF_SECURITY_TOKEN, 
        domain=SF_DOMAIN
    )
    sf = Salesforce(session_id=session_id, instance=instance)
    st.success("Connected to Salesforce successfully!")
except Exception as e:
    st.error(f"Failed to connect to Salesforce: {e}")

# Secret word password
SECRET_WORD = "your_secret_word"  # Replace with your actual secret word

# Title of the application
st.title("Secure Request Form")

# Prompt for the secret word
secret_input = st.text_input("Enter the secret word to access the form:", type="password")

# Check if the secret word is correct
if secret_input == SECRET_WORD:
    st.success("Secret word accepted! You may proceed with the form.")
    
    # Display the form with the specified fields
    with st.form(key='request_form'):
        first_name = st.text_input("First Name")
        middle_name = st.text_input("Middle Name")
        last_name = st.text_input("Last Name")
        preferred_email = st.text_input("Preferred Email Address")
        job_title = st.text_input("Job Title")
        practice_name = st.text_input("Practice Name")
        practice_address = st.text_input("Practice Address")
        supervisor_name = st.text_input("Supervisor Full Name")
        reasoning = st.text_area("Reasoning behind Request")
        
        # Modified question with radio buttons for Yes/No
        has_urmc_account = st.radio(
            "Already have URMC account for eRecords or prior engagement?",
            options=["Yes", "No"]
        )

        # Submit button
        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            # Create a Case object in Salesforce
            try:
                case = sf.Case.create({
                    'Subject': f"Request from {first_name} {last_name}",
                    'Description': reasoning,
                    'SuppliedEmail': preferred_email,
                    'SuppliedName': f"{first_name} {middle_name} {last_name}",
                    # Replace 'Custom_Field__c' with your Salesforce field name
                    'Custom_Field__c': 'Yes' if has_urmc_account == 'Yes' else 'No'  
                })
                st.success("Form submitted successfully and Case created in Salesforce!")
                # Display submitted data for review
                st.write("Here's what you've submitted:")
                st.write({
                    "First Name": first_name,
                    "Middle Name": middle_name,
                    "Last Name": last_name,
                    "Preferred Email Address": preferred_email,
                    "Job Title": job_title,
                    "Practice Name": practice_name,
                    "Practice Address": practice_address,
                    "Supervisor Full Name": supervisor_name,
                    "Reasoning behind Request": reasoning,
                    "Has URMC account": has_urmc_account
                })
            except Exception as e:
                st.error(f"Failed to create Case in Salesforce: {e}")

else:
    if secret_input:
        st.error("Incorrect secret word. Please try again.")
