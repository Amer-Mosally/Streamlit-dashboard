import streamlit as st

from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import streamlit_authenticator as stauth
import database as db


# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")


# --- USER AUTHENTICATION ---
users = db.fetch_all_users()

usernames = [user["key"] for user in users]
names = [user["name"] for user in users]
hashed_passwords = [user["password"] for user in users]

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
"Safseer_LoRa", "abcdef", cookie_expiry_days=1)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    # ---- READ EXCEL ----
    df = pd.read_csv('Test2.csv')

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

        selectedNode = st.radio(
            "Select Node:",
            df["ID"].drop_duplicates())

        st.write("#")

        # Select the choosen node
        df2 = df.query(f"ID == {selectedNode}")
        st.write(df2.iloc[-2:-1])# the one before the last
        st.write(df2.iloc[-1:])  # the one  the last

        st.write(df2.iloc[-2:-1,2:3])
        st.write(df2.iloc[-1]['Temperature'] - df2.iloc[-2]['Temperature'])

        # Get the recent reading
        df2['Date'] = pd.to_datetime(df2['Date'])
        most_recent_date = df2['Date'].max()

        st.write(most_recent_date)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric(f"Recent Reading (Node {selectedNode})", f"{most_recent_date}")
        col2.metric("Temperature", "70 °C", f"{df2.iloc[-1]['Temperature'] - df2.iloc[-2]['Temperature']} °C")
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
        st.title(f"Logging")
        st.write("HERE put select the node")

        data = df.iloc[:,:]

        data_load_state = st.text('Loading data...')
        data_load_state.text("")
        st.write(data)

        st.markdown("`Data Units`: **Temperature (°C)**,  **Humidity (%)**,  **Battery (%)**")

    authenticator.logout("Logout", "main")