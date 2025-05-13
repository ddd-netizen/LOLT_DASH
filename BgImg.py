import streamlit as st
import base64
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Function to encode image to base64
def get_base64_of_bin_file(bin_file_path):
    with open(bin_file_path, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Function to set background image using CSS
def set_background(image_file):
    encoded_image = get_base64_of_bin_file(image_file)
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{encoded_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Call the function with your image file
set_background(r"C:\Users\LOLT\OneDrive\Desktop\Streamlit\loltbg.jpg")  # Replace with your actual image path

# Streamlit content
st.title("Light Of Life Trust")
st.write("This is an example of using a custom background.")

import base64

# Load the Excel file
df= r"C:\Users\LOLT\OneDrive\Desktop\Streamlit\DashBoard LOLT 24-25.xlsx"
excel_file = pd.ExcelFile(df)
print(excel_file.sheet_names)
sheet_options = ["Anando"]


df1 = excel_file.parse('Anando')
df3 = excel_file.parse('MMU')
df4 = excel_file.parse('Livelihood')
df5 = excel_file.parse('Environment')

for Anando in excel_file.sheet_names:
    df = excel_file.parse('Anando')
    print(f"Data from {'Anando'}:")
    print(df.head())  # or process df as needed

for MMU in excel_file.sheet_names:
    df3 = excel_file.parse('MMU')
    print(f"Data from {'MMU'}:")
    print(df.head())  # or process df as needed

    #Total Student count of Anando sheet
    total_students = len(df1)
print(f"Total number of students: {total_students}")

combined_df = pd.concat([df1,df3], ignore_index=True)

total_students = combined_df['Sr.No.'].nunique()  # replace 'StudentID' with actual column name
print(f"Total number of unique students: {total_students}")

print(df.columns)

 #Create for Districts

col1,col2=st.columns((2))
st.sidebar.header("Choose your Filter:")

district =st.sidebar.multiselect("Pick your District",df["District"].unique())
if not district :
        df2=df.copy()
else:

       df2=df[df["District"].isin(district)]

       
    #Create for Taluka

tehsil=st.sidebar.multiselect("Pick Your Center",df2["Tehsil"].unique())
if not tehsil:
        df3=df2.copy()
else:
        df3=df2[df2["Tehsil"].isin(tehsil)]

        #Create for Center
center=st.sidebar.multiselect("Pick Your Center",df3["Center"].unique())


#filtered date based on District and Center
if not district and not tehsil and not center :
 filtered_df =df

elif not tehsil and not center:
    filtered_df=df[df["District"].isin(district)]

elif not district and not center:
    filtered_df=df[df["Tehsil"].isin(tehsil)]

elif tehsil and center:
   filtered_df=df3[df["Tehsil"].isin(tehsil) & df3["Center"].isin(center)]

elif district and center:
   filtered_df=df3[df["District"].isin(district) & df3["Center"].isin(center)]

elif district and tehsil:
   filtered_df=df3[df["District"].isin(district) & df3["Tehsil"].isin(tehsil)]

elif district and center:
   filtered_df=df3[df["District"].isin(district) & df3["Center"].isin(center)]
elif center:
  filtered_df=df3[df["Center"].isin(center)]
                
else:
  filtered_df=df3[df["District"].isin(district) & df3["Tehsil"].isin(tehsil) & df3["Center"].isin(center)]

gender_count = filtered_df['Gender'].value_counts()
gender_counts = filtered_df.groupby(['District','Gender',]).size().reset_index(name='Count')
emp_stauts=filtered_df.groupby(['Gender','Employment Status']).size().reset_index(name='Count')
with col1:
    st.subheader("Gender count")
    fig = px.bar(gender_counts, 
             x='District', 
             y='Count',
             color='Gender', 
             barmode='group', 
             title='Gender Distribution Across Districts',
             template='seaborn')
    st.plotly_chart(fig,use_container_width=True, height = 200)
   
#
# REgion wise sale
with col2:

    st.subheader("Employment Status")
    fig=px.pie(emp_stauts,values="Count", names="Employment Status", hole=0.5, width=600, height=400)
    fig. update_traces(text=filtered_df["District"], textposition="outside")
    st.plotly_chart(fig,use_container_width=True)


 

anando = excel_file.parse("Anando")
total_students = len(anando)
st.sidebar.write("Total Students:", total_students)

