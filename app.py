# Imports
import streamlit as st
import pandas as pd
import os 
from io import BytesIO
import matplotlib.pyplot as plt
# Set up our App
st.set_page_config(page_title="DataFlow Pro by Urooj Saeed", layout="wide" )
st.title("DataFlow Pro")
st.write("Effortlessly clean, convert, and visualize your data—turn raw files into insights with a single click!")

uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # Display info about the file
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size/1024}")

        # Show 5 rows of our df
        st.write("Preview the Head of the Dataframe")
        st.dataframe(df.head())

        # Options for data cleaning 
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"): 
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Removed Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")

                with col2:
                    if st.button(f"Fill Missing Values for {file.name}"):
                        numeric_cols = df.select_dtypes(include=['number']).columns
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.write("Missing Values have been Failled!")

        # Choose Specific Columns to Keep or Convert
        st.subheader("Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Create Some Visualizations
        st.subheader("Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            chart_type = st.radio("Select Chart Type:", ["Bar Chart", "Histogram", "Line Chart", "Scatter Plot", "Area Chart"], key=f"chart_{file.name}")
            
            if chart_type == "Bar Chart":
                st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])
            elif chart_type == "Histogram":
                fig, ax = plt.subplots(figsize=(5, 3))
                df.iloc[:, :2].plot(kind='hist', bins=20, alpha=0.7, ax=ax)
                ax.set_xlabel(df.columns[0])
                ax.set_ylabel("Frequency")
                st.pyplot(fig)
            elif chart_type == "Line Chart":
                fig, ax = plt.subplots(figsize=(5, 3))
                df.iloc[:, :2].plot(kind='line', ax=ax)
                ax.set_xlabel(df.columns[0])
                ax.set_ylabel(df.columns[1])
                st.pyplot(fig)
            elif chart_type == "Scatter Plot":
                fig, ax = plt.subplots(figsize=(5, 3))
                ax.scatter(df.iloc[:, 0], df.iloc[:, 1])
                ax.set_xlabel(df.columns[0])
                ax.set_ylabel(df.columns[1])
                st.pyplot(fig)
            elif chart_type == "Area Chart":
                fig, ax = plt.subplots(figsize=(5, 3))
                df.iloc[:, :2].plot(kind='area', ax=ax, alpha=0.5)
                ax.set_xlabel(df.columns[0])
                ax.set_ylabel(df.columns[1])
                st.pyplot(fig)

        # Convert the File -> CSV to Excel 
         # Convert the File -> CSV to Excel 
        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocumnet.spreadsheetml.sheet"
            buffer.seek(0)

            # Download Button
            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )         

st.success("All files processed!")
