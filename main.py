import streamlit as st
 
st.title('Hello World')
st.subheader('This is a subheader')
 
#take input from user in streamlit
name=st.text_input('Enter your name')
 
#display the input
st.write('Hello',name)
 
#take maths marks in input as slider and display it with name of the student
maths=st.slider('Enter your maths marks',0,100)
st.write(name,'scored',maths,'marks in maths')
 
#give radio button to choose either for gre or gmat display the selected option
exam=st.radio('choose an exam',['GRE','GMAT'])
st.write('You chose',exam)
 
#give checkbox to choose the subjects and display the selected subjects
subjects=st.multiselect(
    'Choose your subjects',['Maths','Physics','Chemistry','PE'])
st.write('You chose',subjects)
 
import pandas as pd
uploaded_file=st.file_uploader('Choose a file',type='xlsx')
 
if uploaded_file is not None:
    df=pd.read_excel(uploaded_file)
    st.write(df)
