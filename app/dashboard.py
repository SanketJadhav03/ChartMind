import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ============================
# 🧠 ChartMind - Data Visualization & AI Insight Generator
# ============================

def run():
    # Page Configuration
    st.set_page_config(page_title="ChartMind", layout="wide")  # Set page title and layout

    # Header
    st.title("📊 ChartMind - Data Visualization & AI Insight Generator")

    # File Uploader
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

    if uploaded_file:
        try:
            # Load DataFrame from CSV
            df = pd.read_csv(uploaded_file)
            st.success("✅ File uploaded successfully!")
            st.dataframe(df)  # Show the uploaded dataset

            # ============================
            # 🔥 AI INSIGHT GENERATOR
            # ============================
            st.subheader("🧠 Advanced AI Insight Generator")

            numeric_df = df.select_dtypes(include=['number'])

            if not numeric_df.empty:
                insights = []

                # 1. **Correlation Analysis**
                st.markdown("### 🔗 Correlation Analysis")
                corr_matrix = numeric_df.corr()
                st.write(corr_matrix)  # Displaying the correlation matrix

                # Finding strong correlations
                top_corr = corr_matrix.unstack().sort_values(ascending=False).drop_duplicates()
                top_corr = top_corr[(top_corr < 0.99) & (top_corr > 0.5)]

                if not top_corr.empty:
                    for pair, corr in top_corr.items():
                        # insights.append(f"📌 **{pair[0]}** and **{pair[1]}** have a strong correlation of **{corr:.2f}**")
                        st.write(f"📌 **{pair[0]}** and **{pair[1]}** have a strong correlation of **{corr:.2f}**")
                else:
                    # insights.append("📍 No strong correlations found between numeric columns.")
                    st.write("📍 No strong correlations found between numeric columns.")

                # 2. **Outlier Detection** using IQR (Interquartile Range)
                st.markdown("### 🔍 Outlier Detection (IQR Method)")
                for column in numeric_df.columns:
                    Q1 = numeric_df[column].quantile(0.25)
                    Q3 = numeric_df[column].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    outliers = numeric_df[(numeric_df[column] < lower_bound) | (numeric_df[column] > upper_bound)]
                    
                    if not outliers.empty:
                        # insights.append(f"📍 **Outliers detected** in column **{column}**: {len(outliers)} outlier values")
                        st.write(f"📍 **Outliers detected** in column **{column}**: {len(outliers)} outlier values")
                    else:
                        # insights.append(f"✅ No outliers detected in column **{column}**")
                        st.write(f"✅ No outliers detected in column **{column}**")
                # 3. **Statistical Summary** of each numeric column
                st.markdown("### 📊 Statistical Summary")
                st.write(numeric_df.describe())

                # 4. **Trend Analysis** (Looking for trends based on first column)
                st.markdown("### 📈 Trend Analysis")
                trend_column = st.selectbox("Select column for trend analysis", numeric_df.columns)
                trend_data = numeric_df[trend_column]

                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(trend_data)
                ax.set_title(f"Trend of {trend_column}")
                ax.set_xlabel("Index")
                ax.set_ylabel(trend_column)
                st.pyplot(fig)

                # 5. **Heatmap Visualization of Correlation Matrix**
                st.markdown("### 🔥 Heatmap of Correlation Matrix")
                fig, ax = plt.subplots(figsize=(10, 8))
                sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
                st.pyplot(fig)

                 

            else:
                st.warning("No numeric columns available for analysis.")
            
            # ============================
            # 🎨 Interactive Charts
            # ============================
            st.subheader("📊 Create Your Own Chart")

            # Column selection for charts
            all_columns = df.columns.tolist()
            numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

            chart_type = st.selectbox("Choose chart type", ["Bar", "Pie", "Line", "Scatter"])

            # Interactive chart generation based on selected chart type
            if chart_type == "Pie":
                pie_column = st.selectbox("Select column for Pie Chart", all_columns)
                pie_data = df[pie_column].value_counts()

                fig, ax = plt.subplots()
                ax.pie(pie_data.values, labels=pie_data.index, autopct="%1.1f%%", startangle=90)
                ax.axis('equal')
                st.pyplot(fig)

            else:
                x_col = st.selectbox("X-axis", all_columns)
                y_col = st.selectbox("Y-axis (Numeric only)", numeric_columns)

                fig, ax = plt.subplots()

                if chart_type == "Bar":
                    ax.bar(df[x_col], df[y_col])
                    ax.set_xlabel(x_col)
                    ax.set_ylabel(y_col)

                elif chart_type == "Line":
                    ax.plot(df[x_col], df[y_col])
                    ax.set_xlabel(x_col)
                    ax.set_ylabel(y_col)

                elif chart_type == "Scatter":
                    ax.scatter(df[x_col], df[y_col])
                    ax.set_xlabel(x_col)
                    ax.set_ylabel(y_col)

                st.pyplot(fig)

        except Exception as e:
            st.error(f"Error reading file: {e}")
    
    else:
        st.info("📤 Please upload a CSV file to begin.")
