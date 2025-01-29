# Vesper Project

## Prerequisites

1. **Python Environment**:
   - Python 3.9 or later
   - Install dependencies:
     ```bash
     pip install mysql-connector-python
     ```

2. **MySQL Database**:
   - Install MySQL and ensure the server is running.
   - Create a database named `vesper` (or your desired name):
     ```sql
     CREATE DATABASE vesper;
     ```

3. **Project Setup**:
   - Clone this project or copy the relevant files to your local machine.
   - Navigate to the project directory.

# Data Generation for Customer Segmentation

This project provides a script to generate and populate a MySQL database with customer segmentation data, including `InputFields`, `MacroSegmentation`, `MicroSegmentation`, and `CustomerJourney`.

---

## Configuration

### Database Connection
Update the database credentials in the script to match your MySQL configuration:
```python
app = DataGen(host="localhost", user="root", password="your_password", database="vesper")
```

---

## Running the Script

1. **Run the Script**:
   Execute the script to generate and populate data:
   ```bash
   python -m segmentation.data_generation
   ```

2. **Script Workflow**:
   - Connects to the MySQL database.
   - Resets the database by dropping existing tables.
   - Creates tables: `input_fields`, `macro_segmentation`, `micro_segmentation`, and `customer_journey`.
   - Generates and inserts the specified number of data points into the database.

3. **Verify the Output**:
   - Check the console for logs indicating the successful connection, table creation, and data generation.
   - Example Output:
     ```
     Connection to the database was successful!
     Database reset successfully!
     5 data points successfully generated and stored in MySQL.
     ```

4. **View Data in MySQL**:
   Use MySQL Workbench or a MySQL CLI tool to inspect the tables and data:
   ```sql
   USE vesper;
   SELECT * FROM input_fields;
   SELECT * FROM macro_segmentation;
   SELECT * FROM micro_segmentation;
   SELECT * FROM customer_journey;
   ```

---

## Customization

### Number of Data Points
Change the number of data points to generate by modifying the argument in `generate_and_store_multiple_customer_data`:
```python
app.generate_and_store_multiple_customer_data(10)  # Generate 10 data points
```

### Database Name
Change the database name in the `DataGen` initialization:
```python
app = DataGen(host="localhost", user="root", password="your_password", database="your_database")
```
Ensure the database exists before running the script.

---



---
