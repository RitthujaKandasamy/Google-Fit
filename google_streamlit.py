from tkinter import font
from turtle import right
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests
import sqlite3





# [theme]                                   # storing in config.toml in streamlit

# primaryColor = '#FF4B4B'                  # Primary accent for interactive elements
# backgroundColor = '#EADA9A'               # Background color for the main content area
# secondaryBackgroundColor = '#8DC356'      # Background color for sidebar and most interactive widgets
# textColor = '#31333F'                     # Color used for almost all text

# # Font family for all text in the app, except code blocks
# # Accepted values (serif | sans serif | monospace)
# # Default: "sans serif"
# font = "Serif"




# DB Management, to store data
conn = sqlite3.connect('data.db')
info_data = conn.cursor()


def create_usertable():
    info_data.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT)')

def add_userdata(username, password):
   info_data.execute('INSERT INTO userstable(username, password) VALUES(?,?)', (username,password))
   conn.commit()

def login_user(username,password):
    info_data.execute('SELECT * FROM userstable WHERE username = ? AND password = ?', (username,password))
    data = info_data.fetchall()
    return data


def view_all_users():
    info_data.execute('SELECT * FROM userstable')
    data = info_data.fetchall()
    return data





# app logo
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

with st.sidebar:

     lottie_url = "https://assets3.lottiefiles.com/packages/lf20_sfpilpqw.json"
     lottie_json = load_lottieurl(lottie_url)
     st_lottie(lottie_json)




# sign in 
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_signin = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_mjlh3hcy.json")
lottie_signup = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_q5pk6p1k.json")





# Menu
with st.sidebar:
    
    app_mode = option_menu(None, ["Home", "Sign in", "Create an account"],
                        icons=['house', 'person-circle', 'person-plus'],
                        menu_icon="app-indicator", default_index=0,
                        styles={
        "container": {"padding": "5!important", "background-color": "#f0f2f6"},
        "icon": {"color": "orange", "font-size": "28px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#2C3845"},
    }
    )





# Home page
if app_mode == 'Home':
    st.title('Model for Fitness Software using TMD dataset')
    st.image("Downloads\\fit.jpg", use_column_width = True)
    
    # it use to read and upload the file

# uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files = True)
# for uploaded_file in uploaded_files:
#      data = pd.read_csv(uploaded_file)
#      st.write("filename:", uploaded_file.name)
#      st.write(data)





# Sign in
elif app_mode == 'Sign in':
    st.title("Run for your Life")
    st.write("---")

    left_column, right_column = st.columns(2)               # to get two columns

    with right_column:
        st.subheader("Login")
        username = st.text_input("User Name")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            create_usertable()
            result = login_user(username, password)
            
            if result:
               st.success("You have loged successfully")

            else:
                st.warning("Incorrect Username/Password")
        #st.warning("Please enter your username and password")
    

    with left_column:
         st_lottie(lottie_signin, height=300, key="coding")







# create an account
elif app_mode == 'Create an account':
    st.title("Run for your Life")
    st.write("---")

    left_column, right_column = st.columns(2)               # to get two columns

    with right_column:
        st.subheader("Create New Account")
        new_username = st.text_input("User Name")
        new_password = st.text_input("Password", type="password")

        if st.button("Signup"):
            create_usertable()
            result1 = add_userdata(new_username, new_password)

    st.warning("Please enter your username and password")


    with left_column:
         st_lottie(lottie_signup, height=300, key="coding")


    


