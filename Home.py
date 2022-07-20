import streamlit as st

from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import streamlit_authenticator as stauth
import database as db




import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth  # pip install streamlit-authenticator


# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")


# --- USER AUTHENTICATION ---
users = db.fetch_all_users()

usernames = [user["key"] for user in users]
names = [user["name"] for user in users]
hashed_passwords = [user["password"] for user in users]

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "Safseer-LoRa", "abcdef", cookie_expiry_days=1)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    # ---- READ EXCEL ----
    authenticator.logout("Logout", "main") #logout button on the main body not "sidebar"

    st.title(f"Welcome {name}")
    #horizontal menu
    selected = option_menu(None, ["Dashboard", "Log",],
        icons=['display', 'cloud-fill'],
        menu_icon="cast", default_index=0, orientation="horizontal")


    DATE_COLUMN = 'date/time'
    DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
                    'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

    #*******
    if selected =="Dashboard":
        st.title(f"{selected}")
        st.write("###")   # extra line to separate

        genre = st.radio(
            "Select Node:",
            ('Node 1', 'Node 2', 'Node 3'))

        st.write("#")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Recent Timestamp", "10:30 Pm")
        col2.metric("Temperature", "70 °F", "1.2 °F")
        col3.metric("Humidity", "86%", "4%")
        col4.metric("Battery", "95%", "-5%")

        st.write("###")  # extra line to separate

        d = st.date_input( "Select Date:")
        st.write('Your Date is:        (DELETE ME) ', d)

        st.write("###")  # extra line to separate

        @st.cache
        def load_data(nrows):
            data = pd.read_csv(DATA_URL, nrows=nrows)
            lowercase = lambda x: str(x).lower()
            data.rename(lowercase, axis='columns', inplace=True)
            data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
            return data

        data = load_data(10000)

        st.subheader('Temperature per hour')
        hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
        st.bar_chart(hist_values)

        st.subheader('Nodes Temperature per hour')
        chart_data = pd.DataFrame(np.random.randn(25, 3) , columns=['Node 1', 'Node 2', 'Node 3'])
        st.line_chart(chart_data)

    #*******
    if selected =="Log":
        st.title(f"Raw data")


        @st.cache
        def load_data(nrows):
            data = pd.read_csv(DATA_URL, nrows=nrows)
            lowercase = lambda x: str(x).lower()
            data.rename(lowercase, axis='columns', inplace=True)
            data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
            return data

        data_load_state = st.text('Loading data...')
        data = load_data(10000)
        data_load_state.text("")

        st.write(data)

        df = pd.DataFrame(
            np.random.randn(50, 20),
            columns=('Node %d' % i for i in range(20)))

        st.dataframe(df)  # Same as st.write(df)
