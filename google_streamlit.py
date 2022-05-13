import streamlit as st
import pandas as pd
from time import sleep
from utilities import select_columns
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests
import sqlite3
import joblib
import streamlit.components.v1 as stc
import base64



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
    x=1
    return x

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
lottie_logout = load_lottieurl("https://assets1.lottiefiles.com/private_files/lf30_tapgoijy.json")







def logged_in():


    # MODEL INTEGRATION

    # 1. load model
    model = joblib.load('model.joblib')

    # 2. load data
    data = pd.read_csv('example_file_user.csv')

    # 3. feature selection
    keep_columns = 'accelerometer|sound|gyroscope'
    data = select_columns(data, keep_columns)

    # 4. Prediction
    col1, buff, col2 = st.columns([2, 1, 2])
    with col2:
        demo = st.radio('Prediction demo', ['start', 'stop'], index=1)
        with col1:
            for _, row in data.iterrows():
                if demo == 'start':
                    placeholder = st.empty()
                    pred = model.predict(row.values.reshape(1, -1))[0]

                    if pred == 'walking':
                        placeholder.image(
                            'Downloads/walking.jpg', use_column_width=True,
                            caption=pred)
                        # activities_counts['walking'] += 1

                    elif pred == 'still':
                        placeholder.image(
                            'Downloads/standing.jpg', use_column_width=True,
                            caption=pred)

                        # activities_counts['still'] += 1

                    else:
                        placeholder.image(
                            'Downloads/public_transport.jpg', use_column_width=True,
                            caption=pred)
                        # activities_counts['bus_car_train'] += 1

                else:
                    break

                sleep(2)
                placeholder.empty()



     # create new data input 
    st.subheader("Your weight ")                                            # for weight using session_state
    def lbs_to_kg():
         st.session_state.kg = st.session_state.lbs/2.2046

    def kg_to_lbs():
         st.session_state.lbs = st.session_state.kg*2.2046

    col1, buff, col2 = st.columns([2, 1, 2])
    with col1:
        pounds = st.number_input("Pounds:", key= "lbs", on_change= lbs_to_kg)
    with col2:
        kilograms = st.number_input("Kilograms:", key= "kg", on_change= kg_to_lbs)
    
     
     
     # create activate time
    st.subheader("Time of the activity")
    def hrs_to_min():
         st.session_state.min = st.session_state.hrs*60

    def min_to_hrs():
         st.session_state.hrs = st.session_state.min/60

    col1, buff, col2 = st.columns([2, 1, 2])
    with col1:
        hour = st.number_input("Hour:", key= "hrs", on_change= hrs_to_min)
    with col2:
        time = st.number_input("Minutes:", key= "min", on_change= min_to_hrs)

    
    
    # activate selecting
    st.subheader("Activity")
    option = st.selectbox(
     'Activity:',
     ('📺 watching TV', '🚘 driving', '🧍standing', '🚶walking'))

    st.write('You selected:', option)

    
    if option == '📺 watching TV':
         MET = 1
         st.write('Your MET is :', MET)
    elif option == '🧍standing':
         MET = 1.5
         st.write('Your MET is :', MET)
    elif option == '🚶walking':
         MET = 3.8
         st.write('Your MET is :', MET)
    elif option == '🚘 driving':
         MET = 1.3
         st.write('Your MET is :', MET)
       

    with st.expander("See explanation"):
          st.write("""
         Metabolic Equivalent of a Task (MET) – measures how many times more energy an activity burns in comparison to sitting still for the same period of time (MET = 1).
     """)


    # calculation
    calories = MET * 3.5 * kilograms / 200 
    st.subheader("\n Calories burned per mintues: {} kcal".format(round(calories, 2)))

    calories1 = calories * time
    st.subheader("\n Calories burned: {} kcal".format(round(calories1, 2)))

    loss_weight = calories1 / 7700
    st.subheader("\n Your weight loss: {} kg".format(round(loss_weight, 2)))
     





# Menu

with st.sidebar:
    
    app_mode = option_menu(None, ["Home", "Sign in", "Create an Account","Logout"],
                        icons=['house', 'person-circle', 'person-plus', 'lock'],
                        menu_icon="app-indicator", default_index=0,
                        styles={
        "container": {"padding": "5!important", "background-color": "#f0f2f6"},
        "icon": {"color": "orange", "font-size": "28px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#2C3845"}
    }
    )



if 'app_mode' in st.session_state:
    if app_mode == 'Sign in' or app_mode=='Logged In':
        app_mode = st.session_state.app_mode
    else:
        del st.session_state.app_mode




# Home page
if app_mode == 'Home':
    st.title('**Model for Fitness Software using TMD dataset**')

    # Gif from local file
    file_ = open("C:\\Users\\ritth\\code\\Strive\\Google-Fit\\Images\\gif_test.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()

    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="test gif">',
        unsafe_allow_html=True,
    )

    # Description
    st.markdown('The Aim is to develop a fitness and user transport mode detection software that is able to be used in plug and play style into most apps and smart watches.')
    st.markdown('One of the main ideas behind the project is to facilitate the Transport mode detection and calorie counting and make it more precise.')
    st.write("we had given a raw data, with this we need to train our ML models and try to predict outcomes for the user..")
    
    # Team Img
    #st.image("Images/test.PNG", use_column_width = True)

    # First Plot - Missing value
    st.title('**Finding null-values**')
    #st.image("Images/miss_val.jpg", use_column_width = True)
    st.markdown('ADD A LITTLE DESC')
    
    # Second Plot - Missing value
    st.title('**Target/User**')
    #st.image("Images/compare_user_target.jpg", use_column_width = True)
    st.markdown('u12 and u 6 in test set')

    # Third Plot - Conf. Matrix
    st.title('**Confusion Matrix**')
    #st.image("Images/conf_matrix.jpg", use_column_width = True)
    st.markdown('ADD A LITTLE DESC')

    





# Sign in
elif app_mode == 'Sign in':
    

    # title
    HTML_BANNER = """
    <div style="background-color:#464e5f;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">Welcome back 👋 </h1>
    </div>
    """
    stc.html(HTML_BANNER)

    left_column, right_column = st.columns(2)                     # to get two columns

    with right_column:
        st.subheader("Log in to your account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            create_usertable()
            result = login_user(username, password)
            
            if result:
                st.success("You have logged in successfully")

                if app_mode not in st.session_state:                  # redirect to logged in page
                    st.session_state.app_mode = 'Logged In'
                    st.experimental_rerun()

            else:
                st.warning("Incorrect Username/Password")

    st.info("Don't have an account yet? Sign up")
    
    with left_column:
        st_lottie(lottie_signin, height=300, key="coding")



elif app_mode == 'Logged In':
    

    # title
    HTML_BANNER = """
    <div style="background-color:#464e5f;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">Congratulations. You have logged in succesfully. 👋 </h1>
    </div>
    """
    stc.html(HTML_BANNER)

    logged_in()

    
    



# create an account
elif app_mode == 'Create an Account':
    
    HTML_BANNER = """
    <div style="background-color:#464e5f;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">Reach your Goal 🏋🏃🏊🏻🚵</h1>
    </div>
    """
    stc.html(HTML_BANNER)

    left_column, right_column = st.columns(2)               # to get two columns

    with left_column:
        st_lottie(lottie_signup, height=300, key="coding")

    with right_column:
        st.subheader("Create an Account")
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type="password")

        if st.button("Signup"):
            create_usertable()
            result1 = add_userdata(new_username, new_password)
            
            if result1:
                st.success("You have successfully registered")

            else:
                st.warning("User Registration failed")
                # ding=view_all_users()
                # st.write(ding)

    st.info("Already have an account? Sign in.")






# logout
else:
    st_lottie(lottie_logout)