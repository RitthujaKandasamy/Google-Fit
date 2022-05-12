import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests
import sqlite3
import streamlit.components.v1 as stc



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
lottie_logout = load_lottieurl("https://assets1.lottiefiles.com/private_files/lf30_tapgoijy.json")






# data information(loggedin)
if 'count' not in st.session_state:
    st.session_state.count = 0

def logged_in():
    st.session_state.count += 1
    
     
    HTML_BANNER = """
        <div style="background-color:#464e5f;padding:10px;border-radius:10px">
        <h1 style="color:white;text-align:center;">Google Fit </h1>
        </div>
        """
    stc.html(HTML_BANNER)

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
     ('💃 aerobics', '📺 watching TV', '⚾ baseball,softball', '⛹️ basketball', '🎱 billiards', 
     '🚣‍♂️ rowing', '🚴 cycling', '🕺 dancing', '🚘 driving', '🎣 fishing', '🏌️ golfing',
    '😴 sleeping', '🧍standing', '🏊 swimming', '🚶walking', '🏃 running'))

    st.write('You selected:', option)


    if option == '💃 aerobics':
         MET = 6.83
         st.write('Your MET is :', MET)
    elif option == '📺 watching TV':
         MET = 1
         st.write('Your MET is :', MET)
    elif option == '⚾ baseball,softball':
         MET = 5
         st.write('Your MET is :', MET)
    elif option == '⛹️ basketball':
         MET = 8
         st.write('Your MET is :', MET)
    elif option == '🎱 billiards':
         MET = 2.5
         st.write('Your MET is :', MET)
    elif option == '🧍standing':
         MET = 1.5
         st.write('Your MET is :', MET)
    elif option == '🚣‍♂️ rowing' :
         MET = 4.64
         st.write('Your MET is :', MET)
    elif option == '🚴 cycling':
         MET = 9.5
         st.write('Your MET is :', MET)
    elif option == '🕺 dancing':
         MET = 4.5
         st.write('Your MET is :', MET)
    elif option == '🎣 fishing':
         MET = 4.5
         st.write('Your MET is :', MET)
    elif option == '🏌️ golfing':
         MET = 3.75
         st.write('Your MET is :', MET)
    elif option == '😴 sleeping':
         MET = 1
         st.write('Your MET is :', MET)
    elif option == '🏊 swimming':
         MET = 8
         st.write('Your MET is :', MET)
    elif option == '🚶walking':
         MET = 3.8
         st.write('Your MET is :', MET)
    elif option == '🚘 driving':
         MET = 1.3
         st.write('Your MET is :', MET)
    elif option == '🏃 running':
         MET = 9.8
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
st.write("##")
    




# Menu

with st.sidebar:
    
    app_mode = option_menu(None, ["Home", "Sign in", "Create an account","Logout "],
                        icons=['house', 'person-circle', 'person-plus'],
                        menu_icon="app-indicator", default_index=0,
                        styles={
        "container": {"padding": "5!important", "background-color": "#f0f2f6"},
        "icon": {"color": "orange", "font-size": "28px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#2C3845"}
    }
    )





# Home page
if app_mode == 'Home':
    st.title('**Model for Fitness Software using TMD dataset**')
    st.image("Downloads\\fit.jpg", use_column_width = True)
    
    # it use to read and upload the file

# uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files = True)
# for uploaded_file in uploaded_files:
#      data = pd.read_csv(uploaded_file)
#      st.write("filename:", uploaded_file.name)
#      st.write(data)





# Sign in
elif app_mode == 'Sign in':
    

    # title
    HTML_BANNER = """
    <div style="background-color:#464e5f;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">Welcome back 👋 </h1>
    </div>
    """
    stc.html(HTML_BANNER)

    left_column, right_column = st.columns(2)               # to get two columns

    with right_column:
        st.subheader("Log in to your account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        
        if st.button("Login", on_click=logged_in):
            create_usertable()
            result = login_user(username, password)
            
            if result:
                st.success("You have logged in successfully") 
                
            else:
                st.warning("Incorrect Username/Password")

    st.warning("Please enter your username and password")
    
    with left_column:
        st_lottie(lottie_signin, height=300, key="coding")







# create an account
elif app_mode == 'Create an account':
    
    HTML_BANNER = """
    <div style="background-color:#464e5f;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">Reach your Goal 🏋🏃🏊🏻🚵 </h1>
    </div>
    """
    stc.html(HTML_BANNER)

    left_column, right_column = st.columns(2)               # to get two columns

    with left_column:
        st_lottie(lottie_signup, height=300, key="coding")

    with right_column:
        st.subheader("Create New Account")
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type="password")

        if st.button("Signup", on_click=logged_in):
            create_usertable()
            result1 = add_userdata(new_username, new_password)
            
            if result1:
                st.success("You have successfully registered")

    st.warning("Please enter your username and password")






# logout
else:
    st_lottie(lottie_logout)