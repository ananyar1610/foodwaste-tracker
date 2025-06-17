import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
import seaborn as sns


# Database Connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sadguro161092",
    database="DSB42"
)
cursor = connection.cursor()

# Streamlit Configuration
st.set_page_config(page_title="Local Food Waste Management Dashboard", layout="wide", page_icon="🍽️")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ['Project Introduction', 'Data Overview', 'Visualizations', 'SQL Queries', 'Writer Info'])

if page == 'Project Introduction':
    st.title("🍽️ Local Food Waste Management System")

    # Project Overview
    st.markdown("### 🌐 Project Overview")
    st.markdown("""
    The **Local Food Waste Management System** is designed to support the **redistribution of surplus food**  
    by connecting **providers** (e.g., restaurants, grocery stores) with **receivers** (e.g., NGOs, shelters).  
    The aim is to **reduce food waste** and tackle **community hunger** using structured, data-driven processes.
    """)

    st.image("D:/GUVI2/Foodwastemanagemnt/localfwm.png", caption="Smart Food Redistribution", use_container_width=True)

    # Why This Matters
    st.markdown("### 📍 Why This Matters")
    st.markdown("""
    - Over **1.3 billion tons** of food is wasted globally each year  
    - Millions face **food insecurity** despite available surplus  
    - This system bridges the gap between **excess and need**
    """)

    # Key Features
    st.markdown("### ⚙️ Key Features")
    st.markdown("""
    - City-level tracking of providers and receivers  
    - Real-time listings with expiry visibility  
    - Dashboards to analyze donations and claims  
    - Shelf-life tracking to prevent spoilage  
    - Direct contact access for coordination  
    """)

    st.image("D:/GUVI2/Foodwastemanagemnt/localfwm2.png", caption="From Waste to Worth", use_container_width=True)

    st.markdown("---")

    # Project Objectives
    st.markdown("### 🎯 Project Objectives")
    st.markdown("""
    - Ensure **timely collection and delivery** of surplus food  
    - Use **data analytics** to improve distribution patterns  
    - Enable **transparency** through a SQL-integrated dashboard  
    """)

    # Technologies Used
    st.markdown("### 💻 Technologies Used")
    st.markdown("""
    - **Frontend**: Streamlit  
    - **Database**: MySQL  
    - **Backend**: Python  
    - **Visualization**: Matplotlib, Seaborn, Plotly  
    """)

    st.markdown("---")
    st.success("🔍 Explore the **'SQL Queries'** section to gain insights into food distribution patterns.")





elif page == 'Data Overview':
    st.title("📊 Data Overview")

    st.markdown("""
    Below are the datasets used in the **Local Food Waste Management** system.  
    Use the dropdown to explore the structure and contents of each database table.
    """)

    table = st.selectbox("📁 Select Table", ["providers", "receivers", "foodlistings", "claims"])
    df = pd.read_sql(f"SELECT * FROM {table}", connection)

    st.markdown(f"**📌 Table Selected:** `{table}`")
    st.markdown(f"**Rows:** {df.shape[0]}  **Columns:** {df.shape[1]}")

    

    st.markdown("### 🔍 Table Preview")
    st.dataframe(df, use_container_width=True)

#------------------------------------------------------------------------------------------------------------------
elif page=='Visualizations':
    providers = pd.read_sql("SELECT * FROM providers", connection)
    receivers = pd.read_sql("SELECT * FROM receivers", connection)
    foodlistings = pd.read_sql("SELECT * FROM foodlistings", connection)
    claims = pd.read_sql("SELECT * FROM claims", connection)
    st.title("📊 EDA: Food Sharing System")

    st.header("1. Dataset Overview")
    st.write("**Food Listings:**", foodlistings.shape)
    st.write("**Providers:**", providers.shape)
    st.write("**Receivers:**", receivers.shape)
    st.write("**Claims:**", claims.shape)

    # Show sample data
    with st.expander("Show sample data"):
        st.subheader("Food Listings Sample")
        st.dataframe(foodlistings.head())

        st.subheader("Providers Sample")
        st.dataframe(providers.head())

        st.subheader("Receivers Sample")
        st.dataframe(receivers.head())

        st.subheader("Claims Sample")
        st.dataframe(claims.head())

    # --- Food Listings EDA ---
    st.header("Food Listings Insights")

   

    # Food type breakdown
    if 'Food_Type' in foodlistings.columns:
        fig2 = px.pie(foodlistings, names='Food_Type', title='Food Type Distribution')
        st.plotly_chart(fig2)

    # Meal type
    if 'Meal_Type' in foodlistings.columns:
        meal_counts = foodlistings['Meal_Type'].value_counts().reset_index()
        meal_counts.columns = ['Meal_Type', 'Count']

        fig3 = px.bar(
            meal_counts,
            x='Meal_Type', y='Count',
            labels={'Meal_Type': 'Meal Type', 'Count': 'Count'},
            title="Meal Type Distribution"
        )


    



    # --- Receiver Analysis ---
    st.header(" Receiver Insights")

   
    if 'Type' in receivers.columns:
        fig8 = px.pie(receivers, names='Type', title='Receiver Type Breakdown')
        st.plotly_chart(fig8)

    # --- Claims Overview ---
    st.header("Claim Status Summary")

    if 'Status' in claims.columns:
        fig9 = px.pie(claims, names='Status', title='Claim Status Distribution')
        st.plotly_chart(fig9)

    if 'Timestamp' in claims.columns:
        claims['Timestamp'] = pd.to_datetime(claims['Timestamp'], errors='coerce')
        claims_by_day = claims['Timestamp'].dt.date.value_counts().sort_index()
        fig10 = px.line(x=claims_by_day.index, y=claims_by_day.values,
                        labels={'x': 'Date', 'y': 'Number of Claims'},
                        title='Claims Over Time')
        st.plotly_chart(fig10)
    
    #------------------------------------------------------------------------------------------------------------


elif page == 'SQL Queries':
    st.title("🧮 SQL Queries Dashboard")

    queries = {
        "1. Food providers and receivers in each city": """
        SELECT
            p.City,
            COUNT(DISTINCT p.Provider_ID) AS Num_Providers,
            COUNT(DISTINCT r.Receiver_ID) AS Num_Receivers
        FROM providers p
        LEFT JOIN receivers r ON p.City=r.City
        GROUP BY p.City
        """,

        "2. Food provider type contributing most": """
        SELECT 
            p.Type,
            SUM(f.Quantity) AS Food_Total
        FROM foodlistings f
        JOIN providers p on f.Provider_ID=p.Provider_ID
        GROUP BY p.Type
        ORDER BY Food_Total DESC
        LIMIT 1;
        """,

        "3. Contact info of providers in city": f"""
        SELECT DISTINCT Name,Contact
        FROM providers p
        WHERE City=%s;
        """,

        "4. Receivers who claimed most food": """
        SELECT r.Name, SUM(f.Quantity) AS Food_Claimed
        FROM claims c
        JOIN receivers r ON c.Receiver_ID =r.receiver_ID
        JOIN foodlistings f ON c.Food_ID=f.Food_ID
        WHERE c.Status='Completed' 
        GROUP BY r.Name
        ORDER BY Food_Claimed DESC
        LIMIT 1;
        """,

        "5. Total quantity of food available": """
        SELECT SUM(f.quantity) as Total_Food FROM foodlistings f
        """,

        "6. City with highest food listings": """
        SELECT Location AS City, COUNT(*) AS Max_Listings
        FROM foodlistings
        GROUP BY Location
        ORDER BY Max_Listings DESC
        LIMIT 1;
        """,

        "7. Most commonly available food types": """
        SELECT f.Food_Type, COUNT(*) AS Common_Type
        FROM foodlistings f
        GROUP BY f.Food_Type
        ORDER BY Common_Type DESC
        LIMIT 1;
        """,

        "8. Number of food claims per item": """
        SELECT c.Food_ID, COUNT(*) AS Num_Claims
        FROM claims c
        GROUP BY Food_ID
        ORDER BY Num_Claims DESC;
        """,

        "9. Provider with most successful claims": """
        SELECT p.Provider_ID, COUNT(*) AS Succesful_Claims
        FROM claims c
        JOIN foodlistings f ON c.Food_ID=f.Food_ID
        JOIN providers p ON p.Provider_ID= f.Provider_ID
        WHERE c.Status='Completed'
        GROUP BY p.Provider_ID
        ORDER BY Succesful_Claims DESC
        LIMIT 1;
        """,

        "10. Percentage of claim statuses": """
        SELECT 
                Status,
                COUNT(*) AS count,
                ROUND(100.0*COUNT(*)/(SELECT COUNT(*) FROM claims),2) AS Percentage
        FROM claims
        GROUP BY Status
        ORDER BY Percentage DESC;
        """,

        "11. Avg food claimed per receiver": """
        SELECT r.Name, AVG(f.Quantity) AS Avg_Claimed
        FROM claims c
        JOIN receivers r ON c.receiver_ID=r.receiver_ID
        JOIN foodlistings f ON c.Food_ID=f.Food_ID
        GROUP BY r.Name
        """,

        "12. Most claimed meal type": """
        SELECT Meal_Type, COUNT(*) AS Num_claims
        FROM foodlistings f
        JOIN claims c ON f.Food_ID=c.Food_ID
        GROUP BY Meal_type
        ORDER BY Num_claims DESC
        LIMIT 1;
        """,

        "13. Total food donated per provider": """
        SELECT p.Provider_ID, COUNT(*) AS Num_Donated
        FROM providers p
        JOIN foodlistings f ON p.Provider_ID=f.Provider_ID
        GROUP BY Provider_ID
        ORDER BY Num_Donated;
        """,

        "14. Avg claims per receiver": """
        SELECT Receiver_ID, COUNT(*) AS total_claims
        FROM claims
        GROUP BY Receiver_ID
        """,

        "15. Providers with most diverse offerings": """
        SELECT 
            p.Name AS Pname,
            COUNT(DISTINCT f.Food_type) AS Food_Type_Count
        FROM foodlistings f
        JOIN providers p ON p.Provider_ID =f.Provider_ID
        GROUP BY p.Name
        ORDER BY Food_Type_Count DESC
        LIMIT 1;
        """,

        "16. Top 5 active providers": """
        SELECT 
            p.Provider_ID,
            p.Name as Provider_name,
            COUNT(c.Claim_ID)  AS Claim_num
        FROM providers p
        JOIN foodlistings f ON p.Provider_ID=f.Provider_ID
        JOIN claims c ON f.Food_ID=c.Food_ID
        WHERE c.Status='Completed'
        GROUP BY p.Provider_ID,p.Name
        ORDER BY Claim_num DESC
        LIMIT 5; 
        """,

        "17. Distribution of claim status": """
        SELECT 
            Status,
            COUNT(Claim_ID) AS Claim_Count,
            ROUND(COUNT(Claim_ID)/(SELECT COUNT(*) FROM claims)*100,2) AS Claim_Percentage
        FROM claims 
        GROUP BY Status
        """,

        "18. Providers with no claims": """
        SELECT 
            p.Provider_ID,
            p.Name AS Provider_Name
        FROM providers p
        WHERE NOT EXISTS (
            SELECT 1
            FROM foodlistings f
            JOIN claims c ON f.Food_ID=c.Food_ID
            WHERE f.Provider_ID=p.provider_ID
        );
        """,

        "19. Total claims & quantity per meal": """
        SELECT 
            f.Meal_Type,
            COUNT(c.Claim_ID) AS Total_Claims,
            SUM(f.Quantity) AS Total_Quantity
        FROM claims c
        JOIN foodlistings f ON c.Food_ID=f.Food_ID
        GROUP BY f.Meal_Type, f.Quantity
        ORDER BY Total_Quantity DESC
        """,

        "20. Top 10 provider cities": """
        SELECT 
            p.City AS Provider_city,
            COUNT(*) AS Provider_by_city
        FROM providers p
        GROUP BY p.City
        ORDER BY Provider_by_city DESC
        LIMIT 10
        """,

        "21. Most common receiver type": """
        SELECT 
            r.Type as Receiver_type,
            COUNT(*) AS Receiver_type_count
        FROM receivers r
        GROUP BY r.Type
        ORDER BY Receiver_type_count DESC
        LIMIT 1;
        """,

        "22. Receiver type by count": """
        SELECT 
            r.Type AS Receiver_type,
            COUNT(*) AS Receiver_Type_Count
        FROM receivers r
        GROUP BY r.Type
        ORDER BY Receiver_Type_Count;
        """,

        "23. Receiver count by city": """
        SELECT  
            City AS Receiver_City,
            COUNT(*) AS Receiver_city_count
        FROM receivers
        GROUP BY City
        ORDER BY Receiver_city_count DESC
        """,

        "24. Providers with most expired food": """
        SELECT 
            p.Name AS Provider_Name,
            COUNT(f.Food_ID) AS Expired_food_count
        FROM foodlistings f
        JOIN providers p ON f.Provider_ID=p.Provider_ID
        WHERE f.Expiry_Date<CURDATE()
        GROUP BY p.Provider_ID, p.Name
        ORDER BY Expired_food_count DESC
        LIMIT 5;
        """
    }

    query_choice = st.selectbox("Select SQL Query", list(queries.keys()))

    if "Contact info" in query_choice:
        city_input = st.text_input("Enter City Name")
        if city_input:
            cursor.execute(queries[query_choice], (city_input,))
            df = pd.DataFrame(cursor.fetchall(), columns=["Name", "Contact"])
            st.dataframe(df)
    else:
        cursor.execute(queries[query_choice])
        rows = cursor.fetchall()
        if rows:
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(rows, columns=columns)
            st.dataframe(df)
        else:
            st.write("No data found for the selected query.")

elif page == 'Writer Info':
    #st.title("Sadguru Kripa")
    st.title("🧑‍💻 Developer Information")
    st.markdown("""
    ### 📌 Project Creator  
    **Name:** Ananya R  
    **Project:** Local Food Waste Management System  
    **Role:** Design & Development  
    """)
    
    st.markdown("""
    ### 🔗 Connect  
    - [LinkedIn Profile](https://www.linkedin.com/in/ananyar-80595a269/)
    """)
    st.markdown("---")

    st.markdown("""
    _"This project was built with the aim of optimizing modern data-driven techniques to facilitate quick and efficient management of real-world problems around food waste management."_  
    — *Ananya R*
    """)



else:
    print("Incorrect value error")


