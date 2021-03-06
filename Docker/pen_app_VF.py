import streamlit as st
import pandas as pd
import numpy as np
#import pickle
from sklearn.ensemble import RandomForestClassifier
st.write("""
# Penguin Prediction APP
This app predicts the **Palmer Penguin** species!
Data obtained from the [palmerpenguins library](https://github.com/allisonhorst/palmerpenguins) in R by Allison Horst.
""")
st.sidebar.header('User Input Features')
st.sidebar.markdown('''
[Example CSV input file](https://github.com/HamzaOulaarbi/penguins_heroku/blob/main/Data_Exemple_penguoins.csv)
''')

# user inputs features into DataFrame
uploaded_file=st.sidebar.file_uploader('Upload your input CSV file',type='csv')
def user_input_features():
    island = st.sidebar.selectbox('Island',('Biscoe','Dream','Torgersen'))
    sex = st.sidebar.radio('Sex',('male','female'))
    bill_length_mm = st.sidebar.slider('Bill length (mm)', 32.1,59.6,43.9)
    bill_depth_mm = st.sidebar.slider('Bill depth (mm)', 13.1,21.5,17.2)
    flipper_length_mm = st.sidebar.slider('Flipper length (mm)', 172.0,231.0,201.0)
    body_mass_g =st.sidebar.slider('Body mass (g)', 2700.0,6300.0,4207.0)
    data={'island':island,
          'bill_length_mm':bill_length_mm,
          'bill_depth_mm': bill_depth_mm,
          'flipper_length_mm': flipper_length_mm,
          'body_mass_g': body_mass_g,
          'sex': sex}
    return pd.DataFrame([data])
if uploaded_file:
    input_df=pd.read_csv(uploaded_file,delimiter=',')
else:
    input_df=user_input_features()

#Encoding=> combines user input features with entire penguins dataset
# This will be useful for the encoding phase
penguins_raw=pd.read_csv('penguin_data.csv',delimiter=';')
penguins = penguins_raw.drop(columns=['species'])
df=pd.concat([penguins,input_df],axis=0)

# Encoding of ordinal features
encode = ['sex','island']
for col in encode:
    dummy = pd.get_dummies(df[col], prefix=col)
    df = pd.concat([df,dummy], axis=1)
    del df[col]
df = df[-1:] # Selects only the last row (the user input data)

# Displays the user input features
st.subheader('User Input features')
if uploaded_file:
    st.write(df)
else:
    st.write('Awaiting CSV file to be uploaded. Currently using example input parameters (shown below).')
    st.write(df)

# Reads in saved classification model
load_clf = pickle.load(open('penguins_clf.pkl', 'rb'))

dict={'Adelie' : 0,
    'Chinstrap': 1,
    'Gentoo':2}
leg=pd.DataFrame(dict.items(),columns=['Species', 'Classes'])
st.subheader('Legend')
st.write(leg)

# Apply model to make predictions
prediction = load_clf.predict(df)
prediction_proba = load_clf.predict_proba(df)
prediction_proba=pd.DataFrame(prediction_proba,columns=['Adelie','Chinstrap','Gentoo'])
st.subheader('Prediction : ')
penguins_species = np.array(['Adelie','Chinstrap','Gentoo'])
st.write(penguins_species[prediction][0])

st.subheader('Prediction Probability')
st.write(prediction_proba)
