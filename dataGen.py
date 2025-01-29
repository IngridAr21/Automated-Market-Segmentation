from flask import Flask
from sqlalchemy import inspect
from backend.database import db
from backend.objects.inputObj import InputFields
from backend.objects.macroObj import MacroSegmentation
from backend.objects.microObj import MicroSegmentation
from backend.objects.journeyObj import CustomerJourney


class DataGen:

    @staticmethod
    def generate_and_store_input_fields(n):

        for _ in range(n):
            input_field = InputFields.generate_inputs()  # Ensure this method exists and returns a valid object
            db.session.add(input_field)
        db.session.commit()

    @staticmethod
    def generate_and_store_macro_segments(input_fields):

        for input_field in input_fields:
            macro_segment = MacroSegmentation.generate_macro(input_field)  # Ensure this method exists
            db.session.add(macro_segment)
        db.session.commit()

    @staticmethod
    def generate_and_store_micro_segments(macro_segments):

        for macro_segment in macro_segments:
            micro_segment = MicroSegmentation.generate_micro(macro_segment)  # Ensure this method exists
            db.session.add(micro_segment)
        db.session.commit()

    @staticmethod
    def generate_and_store_customer_journeys(micro_segments):

        for micro_segment in micro_segments:
            customer_journey = CustomerJourney.generate_customer_journey(micro_segment)  # Ensure this method exists
            db.session.add(customer_journey)
        db.session.commit()

    @staticmethod
    def generate_full_data_pipeline(input_count):

        # Step 1: Generate Input Fields
        DataGen.generate_and_store_input_fields(input_count)

        # Step 2: Generate Macro Segments
        input_fields = InputFields.query.all()
        DataGen.generate_and_store_macro_segments(input_fields)

        # Step 3: Generate Micro Segments
        macro_segments = MacroSegmentation.query.all()
        DataGen.generate_and_store_micro_segments(macro_segments)

        # Step 4: Generate Customer Journeys
        micro_segments = MicroSegmentation.query.all()
        DataGen.generate_and_store_customer_journeys(micro_segments)


    def runDataGen(input_count):
        app = Flask(__name__)

        # Update with your MySQL credentials
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vesper.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.init_app(app)

        with app.app_context():
            db.drop_all()

            created_tables = inspect(db.engine).get_table_names()

            db.create_all()

            created_tables = inspect(db.engine).get_table_names()

            DataGen.generate_full_data_pipeline(input_count=input_count)

            row_count = db.session.query(InputFields).count()

