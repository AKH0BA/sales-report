# Sales Report Automation Project

This project connects **Python**, **PostgreSQL**, and **Excel** to generate automatic sales reports with visual charts.

## What my project does
- Creates and fills a PostgreSQL database using SQL scripts.
- Runs analysis queries through Python.
- Exports results to Excel and saves visual charts (`matplotlib`).
- Organized folder structure for professional reporting.

## 🗂 Folder structure
sales-report/
|- sql/  SQL scripts to create tables and insert data
|- python/  Python scripts for analysis and reporting
|- output/  Generated Excel and chart

## Used Techs
- Python
- SQL
- Excel
- VS code , PG Admin

## How to run
1. Open `sql/01.creating_table.sql` and `sql/02.inserting_data.sql` in **pgAdmin**, then execute them.
2. Update your database password in `python/report.py`.
3. Run the Python file:
   ```bash
   python python/report.py
4. results will appear in output
