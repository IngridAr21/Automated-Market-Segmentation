from sqlalchemy import create_engine, inspect
import pandas as pd

def export_db_to_excel(output_path):
    """Export the database tables to an Excel file."""
    # Correct absolute path to the SQLite database
    database_uri = 'sqlite:////Users/miloudrapers/Desktop/Project 3.1/vesper_project/instance/vesper.db'
    engine = create_engine(database_uri)

    try:
        inspector = inspect(engine)
        table_names = inspector.get_table_names()
        
        if not table_names:

            return


        with pd.ExcelWriter(output_path, engine='openpyxl') as excel_writer:
            for table in table_names:
                query = f"SELECT * FROM {table}"
                df = pd.read_sql(query, con=engine)
                if df.empty:
                    continue
                df.to_excel(excel_writer, sheet_name=table, index=False)

    except Exception as e:
        print(f"Failed to connect to the database or export data: {e}")

if __name__ == "__main__":
    export_db_to_excel("database_output.xlsx")
