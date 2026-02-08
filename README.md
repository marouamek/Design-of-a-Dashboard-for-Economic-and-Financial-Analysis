# Building a Web Dashboard for Economic and Financial Analysis

## Project Overview
This project is part of an in-depth analysis of Consumer Price Index (CPI) data for the period **2015–2024** in **Algiers**.  
Its main goal is to provide an **interactive dashboard** and **data export tools** to explore CPI variations by group and sub-group, as well as overall inflation trends.

The dashboard allows users to analyze economic indicators through dynamic charts and structured insights, making the data more accessible for interpretation and decision-making.

## Course Module
This project was developed as part of the **Advanced Programming** module.

The course aims to help students become familiar with modern Web technologies, including:
- Python programming
- Multimedia Web development
- Web services and APIs

## Key Concepts Used
- **Backend with Flask**
  - Development of REST APIs to retrieve data from a MySQL database.
  - Generation of CSV and Excel files for exporting results.

- **Frontend with JavaScript**
  - Use of Chart.js to display interactive charts (bar charts, line charts, pie charts, donut charts).
  - Handling user interactions (toggle buttons, sliders, dynamic filters).

- **Jinja Templating**
  - Integration of Jinja to dynamically generate HTML templates.
  - Reusability of components (such as the sidebar) to avoid code duplication and ensure consistent structure.

- **Relational Database**
  - Data modeling using dimensional tables (`Dim_Year`, `Dim_Group`, `Dim_SubGroup`) and a fact table (`Fact_CPI`).
  - SQL queries for computing variations, contributions, and trends.

- **Data Visualization**
  - Representation of CPI data through interactive visualizations for better understanding of economic patterns.

- **Data Export**
  - Generation of CSV and Excel files to allow offline analysis.

## Analytical Questions Addressed

### **Synthetic Overview**
1. What is the most inflationary year in Algiers between 2015 and 2024?
2. Which group contributed the most to the CPI increase in 2024?
3. Is there a specific price anomaly related to a particular product in the basket?
4. What was the annual CPI variation in Algiers in 2024 compared to 2023?

### **In-Depth Analysis**
5. How has CPI evolved in Algiers from 2015 to 2024?
6. Is the inflation rate accelerating or slowing down?
7. What were the month-to-month price variations during 2024?
8. How does each group contribute to CPI evolution since 2015?

### **Granular Analysis (Example: Food Group)**
9. What are the three food sub-groups with the most critical inflation rates in 2024?
10. How did the food group contribute to the CPI increase in 2024 compared to other groups?
11. For a given sub-group (e.g., cereals), is the price increase sudden acceleration or a stable trend throughout the year?

## What We Learned From This Project
This project helped us understand that raw data alone is not enough for meaningful analysis.  
To extract value, data must be cleaned, structured, and interpreted within a proper context.

We implemented the **ETL process (Extract, Transform, Load)**:

- **Extract**: Collecting heterogeneous data from ONS reports.
- **Transform**: Cleaning the data, calculating monthly and annual variations, and normalizing formats.
- **Load**: Structuring and storing the data in a star schema (fact and dimension tables) to optimize query performance.

## Technical Skills Developed
- **Backend Development**
  - Building REST APIs with Flask.
  - Managing MySQL database connections and optimizing SQL queries.

- **Frontend Development**
  - Integrating data visualization libraries such as Chart.js.
  - Handling user interactions and dynamically updating HTML components.

- **Data Analysis**
  - Designing a data model to answer analytical questions.
  - Computing variations and contributions from raw CPI data.

## Soft Skills Developed
Beyond technical implementation, this project allowed us to:

1. Interpret complex macroeconomic indicators (CPI, year-on-year variation, weights).
2. Translate real economic concepts into technical data models (from reports to relational databases).
3. Learn how to present data effectively by choosing the most relevant chart type for decision-making.
4. Develop critical thinking toward numerical data by detecting anomalies, seasonal effects, and inflation causes.
5. Gain experience working collaboratively in a multidisciplinary team.

---
This project combines technical and analytical skills to solve real-world challenges related to economic data analysis.
