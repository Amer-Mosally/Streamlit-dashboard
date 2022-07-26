import streamlit as st

from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import streamlit_authenticator as stauth
import database as db


# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
# Insted of :bar_chart: >>> put safseer logo
st.set_page_config(page_title="Safseer", page_icon=":bar_chart:", layout="wide")

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
    # If log in successfully
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
        st.write("###")         # extra line to separate

        selectedNode = st.selectbox(
            "Select Node:",
            df["ID"].drop_duplicates())

        st.write("#")

        # Select the chosen node
        df2 = df.query(f"ID == {selectedNode}")
        #st.write(df2.iloc[-2:-1])              # the one before the last read
        #st.write(df2.iloc[-1:])                # last read

        # Get the recent reading
        #df2['Date'] = pd.to_datetime(df2['Date'])
        most_recent_date = df2['Date'].max()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric(f"Recent Reading (Node {selectedNode})", f"{most_recent_date}")
        col2.metric("Temperature", f"{df2.iloc[-1]['Temperature']} °C", f"{df2.iloc[-1]['Temperature'] - df2.iloc[-2]['Temperature']} °C")
        col3.metric("Humidity", f"{df2.iloc[-1]['Humidity']}%", f"{df2.iloc[-1]['Humidity'] - df2.iloc[-2]['Humidity']} %")
        col4.metric("Battery", f"{df2.iloc[-1]['Battery']}%", f"{df2.iloc[-1]['Battery'] - df2.iloc[-2]['Battery']} %")

        st.write("###")  # extra line to separate

        selectedDate = st.date_input( "Select Date:")

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

        selectedNode = st.selectbox(
            "Select Node:",
            df["ID"].drop_duplicates())

        df2 = df.query(f"ID == {selectedNode}")

        data = df2.loc[:,:] # Will show only the selected node
        st.write(data)

        with open('test2.csv') as f:
            st.download_button(label='Download All Data', data=f, file_name='Amer.csv')  # Defaults to 'text/plain'

        data_load_state = st.text('Loading data...')
        data_load_state.text("")

        st.markdown("`Data Units`: **Temperature (°C)**,  **Humidity (%)**,  **Battery (%)**")

    authenticator.logout("Logout", "main")