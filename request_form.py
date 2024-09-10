import streamlit as st

# Secret word password
SECRET_WORD = "your_secret_word"  # Replace with your actual secret word

# Set the page title and icon
st.set_page_config(page_title="Request Form", page_icon="📝")

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
            st.success("Form submitted successfully!")
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

else:
    if secret_input:
        st.error("Incorrect secret word. Please try again.")
