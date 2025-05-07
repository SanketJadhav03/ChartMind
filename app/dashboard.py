import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from .utils import clean_data
import numpy as np 

def run():
    st.set_page_config(page_title="ChartMind", layout="wide")
    st.title("📊 ChartMind - Visual Analytics Dashboard")

    uploaded_file = st.file_uploader("Upload your dataset (CSV or Excel)", type=["csv", "xlsx"])

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            df = clean_data(df)

            # In the Streamlit section
            st.subheader("🔍 AI Insights Generator") 
            if uploaded_file is not None:
                insights = generate_insights(df)
                if insights:
                    st.write(insights)
                else:
                    st.write("No insights could be generated from the dataset.")

            st.subheader("🔍 Data Preview")
            st.dataframe(df.head())

            st.subheader("📊 Summary Statistics")
            st.write(df.describe())

            st.subheader("📈 Quick Visualization")
            chart_type = st.selectbox("Select chart type", ["Bar Chart", "Line Chart", "Heatmap"])
            col1 = st.selectbox("X-axis column", df.columns)
            col2 = st.selectbox("Y-axis column", df.columns)

            if chart_type == "Bar Chart":
                fig, ax = plt.subplots()
                sns.barplot(data=df, x=col1, y=col2, ax=ax)
                st.pyplot(fig)

            elif chart_type == "Line Chart":
                fig, ax = plt.subplots()
                sns.lineplot(data=df, x=col1, y=col2, ax=ax)
                st.pyplot(fig)

            elif chart_type == "Heatmap":
                fig, ax = plt.subplots()
                
                # Select only numeric columns for correlation
                numeric_df = df.select_dtypes(include=[np.number])
                
                # Generate the correlation matrix
                corr = numeric_df.corr()
                
                # Create a mask for the upper triangle
                mask = np.triu(np.ones_like(corr, dtype=bool)) 
                
                # Plot the heatmap
                sns.heatmap(corr, mask=mask, annot=True, cmap="coolwarm", ax=ax, linewidths=0.5)
                st.pyplot(fig)
            
        except Exception as e:
            st.error(f"Error reading file: {e}")


import pandas as pd
import numpy as np

def generate_insights(df: pd.DataFrame) -> str:
    insights = []

    # Example Insight 1: Average salary by department
    if 'Department' in df.columns and 'Salary' in df.columns:
        avg_salary_by_dept = df.groupby('Department')['Salary'].mean().reset_index()
        highest_avg_salary_dept = avg_salary_by_dept.loc[avg_salary_by_dept['Salary'].idxmax()]
        insights.append(f"The department with the highest average salary is {highest_avg_salary_dept['Department']} with an average salary of ₹{highest_avg_salary_dept['Salary']:,.2f}.")

    # Example Insight 2: Most experienced person
    if 'Experience_Years' in df.columns and 'Name' in df.columns:
        most_experienced = df.loc[df['Experience_Years'].idxmax()]
        insights.append(f"The most experienced person is {most_experienced['Name']} with {most_experienced['Experience_Years']} years of experience.")

    # Example Insight 3: Salary distribution overview
    if 'Salary' in df.columns:
        avg_salary = df['Salary'].mean()
        min_salary = df['Salary'].min()
        max_salary = df['Salary'].max()
        insights.append(f"The salary distribution is between ₹{min_salary:,.2f} and ₹{max_salary:,.2f}, with an average salary of ₹{avg_salary:,.2f}.")

    # Additional insights can be added as needed

    return "\n\n".join(insights)

