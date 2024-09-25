import streamlit as st
import os
import json
import pandas as pd
import plotly.express as px
from datetime import datetime
 
# Define path for storing credentials
CREDENTIALS_FILE = "Credentials.json"
USER_SESSION_FILE = "user_session.json"
 
# Load existing credentials
def load_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as file:
            return json.load(file)
    return {}
 
# Save new credentials
def save_credentials(credentials):
    with open(CREDENTIALS_FILE, "w") as file:
        json.dump(credentials, file, indent=4)
 
# Create user folder
def create_user_folder(email):
    folder_name = email.split('@')[0]  # Folder based on part of email before @
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
 
# Store the logged-in user session
def save_user_session(email):
    with open(USER_SESSION_FILE, "w") as file:
        json.dump({"logged_in": email}, file)
 
# Load user session (if any)
def load_user_session():
    if os.path.exists(USER_SESSION_FILE):
        with open(USER_SESSION_FILE, "r") as file:
            return json.load(file).get("logged_in", None)
    return None
 
# Clear the user session on logout
def clear_user_session():
    if os.path.exists(USER_SESSION_FILE):
        os.remove(USER_SESSION_FILE)
 
# Signup form
def signup():
    st.header("Sign Up")
 
    name = st.text_input("Name")
    phone = st.text_input("Phone")
    dob = st.date_input("DOB", datetime(2000, 1, 1))
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
 
    if st.button("Sign Up"):
        if name and phone and email and password:
            # Load existing credentials
            credentials = load_credentials()
 
            # Check if email already exists
            if email in credentials:
                st.warning("Email is already registered. Please try logging in.")
            else:
                # Save new user details
                credentials[email] = {
                    "name": name,
                    "phone": phone,
                    "dob": str(dob),
                    "password": password
                }
                save_credentials(credentials)
 
                # Create a folder for the user
                create_user_folder(email)
                st.success(f"User {name} signed up successfully!")
        else:
            st.error("Please fill out all fields.")
 
# Login form
def login():
    st.header("Login")
 
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
 
    if st.button("Login"):
        if email and password:
            # Load existing credentials
            credentials = load_credentials()
 
            # Validate user credentials
            if email in credentials and credentials[email]["password"] == password:
                st.success(f"Welcome back, {credentials[email]['name']}!")
                save_user_session(email)
            else:
                st.error("Invalid email or password.")
        else:
            st.error("Please enter both email and password.")
 
# Marks input form for 7 subjects
def input_marks(email):
    st.header(f"Welcome {load_credentials()[email]['name']}")
 
    folder_name = email.split('@')[0]
    file_path = os.path.join(folder_name, "marks.csv")
 
    # Check if marks already exist (to show graphs if user logs back in)
    if os.path.exists(file_path):
        st.info("Marks already submitted! Displaying your results:")
        marks_df = pd.read_csv(file_path)
        display_graphs(marks_df)
    else:
        # Slider inputs for 7 subjects
        subjects = ["Math", "Science", "English", "History", "Geography", "Computer", "Physical Education"]
        marks = {}
        for subject in subjects:
            marks[subject] = st.slider(subject, 0, 100, 50)
 
        # On submit, save the marks to a CSV in the user's folder and plot the graph
        if st.button("Submit"):
            marks_df = pd.DataFrame(marks.items(), columns=["Subject", "Marks"])
            marks_df.to_csv(file_path, index=False)
            st.success("Marks saved successfully!")
            display_graphs(marks_df)
 
# Function to display graphs using Plotly Express
def display_graphs(marks_df):
    st.subheader("Marks Distribution")
 
    # Bar chart using Plotly Express
    bar_fig = px.bar(
        marks_df,
        x='Subject',
        y='Marks',
        title="Marks by Subject",
        labels={'Marks': 'Marks'},
        color='Marks',
        color_continuous_scale='Blues'
    )
    st.plotly_chart(bar_fig)
 
    # Line chart using Plotly Express
    line_fig = px.line(
        marks_df,
        x='Subject',
        y='Marks',
        title="Marks Trend by Subject",
        markers=True
    )
    st.plotly_chart(line_fig)
 
# Main app function with conditional rendering for login, sign up, and user dashboard
def app():
    # Load the currently logged-in user (if any)
    logged_in_user = load_user_session()
 
    if logged_in_user:
        # Display the user's dashboard with a Sign Out button and marks input form
        if st.sidebar.button("Sign Out"):
            clear_user_session()
            st.experimental_rerun()
 
        # Welcome message and marks input
        input_marks(logged_in_user)
    else:
        # Sidebar for navigation between Sign Up and Login
        st.sidebar.title("Navigation")
        option = st.sidebar.radio("Choose an option", ("Sign Up", "Login"))
 
        if option == "Sign Up":
            signup()
        elif option == "Login":
            login()
 
if __name__ == "__main__":
    app()