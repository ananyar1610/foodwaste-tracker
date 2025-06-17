# foodwaste-tracker
This project aims to create a data-driven system to monitor food surplus and coordinate donations between providers and receivers in real time.

## Project workflow
### 1. Data Preparation
-Read csv datasets, namely, providers.csv, receiver.sv, foodlisting.csv and claims.csv
-Clean and standardize data for accuracy and consistency
-Format data 

### 2. Database Creation
-Store data into relational tabes in SQL
-Implement CRUD operations 
  -Create: Insert new datapoints into the tables
  -Read: Fetch new details from datasets
  -Update: Edit datapoints
  -Delete: Remove outdated or invalid datapoints

### 3. Data Analysis
-Run 15+SQL Queries to derive unique insights 

### 4. Application Development
-Build a **Streamlit**-based user interface to:
- Display SQL query results in a user-friendly format.
  - Provide interactive filters: City, Provider, Food Type, Meal Type.
  - Show provider contact details for direct coordination.
  - Support real-time interaction with the SQL database.

 ### 5. Deployment
 -Deploy streamlit app to web
 
 ---

 ## Data Flow & Architecture

### Data Storage
- SQL database contains:
  - Provider & Receiver profiles
  - Food Listings
  - Claims (who claimed what and when)

### Processing Pipeline
- Load CSVs → Clean & Normalize → Insert into SQL
- Analyze → Generate Insights → Visualize via Streamlit

###  Deployment
- Hosted Streamlit interface connects to SQL backend for live interactions.

---

## Datasets Used

| Dataset Name         | Description                               |
|----------------------|-------------------------------------------|
| `providers_data.csv` | Details of food providers (e.g., restaurants, NGOs) |
| `receivers_data.csv` | Information about food seekers/receivers   |
| `food_listings_data.csv` | Listings of available food with expiry info |
| `claims_data.csv`    | Record of which food items have been claimed |

---

## Features

- Data cleaning and ingestion
- SQL schema and operations
- 15 analytical queries
- Streamlit dashboard
- Filters & provider contact visibility
- End-to-end deployment

---

## Sample Queries Included

1. Top 5 cities with most food listings  
2. Food types with highest wastage  
3. Providers with the most donations  
4. Listings expiring in the next 3 days  
5. Receiver demand trends by region  
... and more!

---

## Tech Stack

- **Python 3**
- **MySQL**
- **Pandas**
- **Streamlit**
- **Matplotlib / Seaborn** 

---

## Future Enhancements

- Add user authentication (JWT, OAuth)
- Use cloud database (e.g., Supabase, Firebase)
- Email/SMS notification system for soon-to-expire items
- Mobile-friendly interface

---

## Contributors

- Ananya R - [GitHub][(https://github.com/ananyar1610)]

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.
 
