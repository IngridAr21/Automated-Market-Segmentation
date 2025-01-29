import pandas as pd
from backend.objects.journeyObj import CustomerJourney
from backend.objects.microObj import MicroSegmentation
from backend.objects.macroObj import MacroSegmentation
from backend.objects.inputObj import InputFields
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import LSTM, Dense
import tensorflow as tf
import numpy as np
from flask import Flask
from backend.database import db
import joblib
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Usuario/Documents/vesper_project/instance/vesper.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

custJourneyData = {
    "Awareness": ["Trade Shows/Conferences", "Networking Events", "Business Cards/Merchandise",
                  "Word of Mouth", "Social Media Ads", "Webinars/Online Conferences",
                  "Digital PR / Content Marketing", "Influencer Marketing",
                  "Programmatic Advertising", "Influencer Webinars/Interviews",
                  "Video Ads", "Podcast Appearances/Advertisements"],

    "Consideration": ["Onsite Product Demos", "Workshops/Seminars", "Printed Case Studies/Testimonials",
                      "Industry Awards/Recognition", "Office/Facility Tours", "Website",
                      "Online Demos/Virtual Consultations", "Customer Reviews/Testimonials",
                      "Comparison Tools", "Retargeting Ads", "Interactive Product Configurators",
                      "Interactive FAQ or AI Chatbots"],

    "Decision-Making": ["Face-to-Face Negotiations", "In-Person Product Trials / Meetings",
                        "Third-Party Meetings", "Proposal via Email/Online Portal",
                        "Online Product Demos", "ROI Calculators"],

    "Purchase": ["Face-to-Face Contract Signing", "Product/Service Handover Meeting",
                 "Onsite Delivery or Setup", "E-commerce/Ordering Portals",
                 "E-invoicing", "Dynamic Pricing Tools", "Custom Payment Portals",
                 "Purchase Confirmation Emails"],

    "Service": ["Maintenance Visits", "Dedicated Account Manager", "Help Desk/Support Portal",
                "Online Training/Webinars", "Video Tutorials", "Live Chat/Chatbots for Support"],

    "Loyalty": ["Loyalty Programs (Physical Rewards)", "Customer Appreciation Events",
                "Physical Awards/Recognition", "Branded Gifting Programs",
                "Subscription Services (Digital Renewal)", "Automated Personalization",
                "Automated Renewal Reminders", "Exclusive Access to Content",
                "Loyalty Emails/Discount Offers", "Gamified Loyalty Programs"],

    "Ambassador": ["Referral Program (Physical Rewards)", "Customer Advisory Board (In-Person Meetings)",
                   "Invitations to Product Launches or Corporate Events", "Referral Program (Digital Rewards)",
                   "Social Media Sharing", "Affiliate or Influencer Partnerships"]
}

columns = ['age', 'gender', 'location', 'education_level', 'technology_used', 'job_title', 'experience_level',
           'functional_field', 'decision_making_role',
           'work_environment', 'professional_network', 'risk_tolerance', 'decision_making_style', 'motivations',
           'personality_traits', 'pain_points', 'kpis', 'challenges', 'goals'
           ]

journey_stages = ["Awareness", "Consideration", "Decision-Making", "Purchase", "Service", "Loyalty", "Ambassador"]

# IMPORTANT for encoding
label_encoders = {}
models = {}


class CustomerJourneyModel:

    @staticmethod
    def fetch_data():
        with app.app_context():
            micros = MicroSegmentation.query.all()
            customerjourneys = CustomerJourney.query.all()

            micro_data = [
                [
                    # mic.macro_segmentation_id,
                    mic.age,
                    mic.gender,
                    mic.education_level,
                    mic.technology_used,
                    mic.job_title,
                    mic.experience_level,
                    mic.functional_field,
                    mic.decision_making_role,
                    mic.work_environment,
                    mic.professional_network,
                    mic.risk_tolerance,
                    mic.decision_making_style,
                    mic.motivations,
                    mic.personality_traits,
                    mic.pain_points,
                    mic.kpis,
                    mic.challenges,
                    mic.goals,
                ]
                for mic in micros
            ]

            customerjourney_data = [
                [
                    cs.awareness,
                    cs.consideration,
                    cs.decision_making,
                    cs.purchase,
                    cs.service,
                    cs.loyalty,
                    cs.ambassador
                ]
                for cs in customerjourneys
            ]

            micro_columns = [
                "age", "gender", "education_level", "technology_used",
                "job_title", "experience_level", "functional_field", "decision_making_role",
                "work_environment", "professional_network", "risk_tolerance", "decision_making_style",
                "motivations", "personality_traits", "pain_points", "kpis", "challenges", "goals"
            ]

            customerjourney_columns = [
                "awareness", "consideration", "decision_making",
                "purchase", "service", "loyalty", "ambassador"
            ]

            micro_df = pd.DataFrame(micro_data, columns=micro_columns)
            customerjourney_df = pd.DataFrame(customerjourney_data, columns=customerjourney_columns)

            combined_df = pd.concat([micro_df, customerjourney_df], axis=1)

            return combined_df

    def __repr__(self):
        return (
            f"JourneySegmentationService(\n"
            f"  Micro Segmentation: {self.micro_segmentation},\n"
            f"  Awareness: {self.awareness},\n"
            f"  Consideration: {self.consideration},\n"
            f"  Decision-Making: {self.decisionMaking},\n"
            f"  Purchase: {self.purchase},\n"
            f"  Service: {self.service},\n"
            f"  Loyalty: {self.loyalty},\n"
            f"  Ambassador: {self.ambassador}\n"
            f")"
        )

    @staticmethod
    def encoding(df):
        for column in df.columns:
            le = LabelEncoder()
            df[column] = le.fit_transform(df[column].astype(str))
            label_encoders[column] = le


        return df

    # --------------
    # Training
    # --------------

    def train_model(self, df):
        # Split data into X and Y
        X = df.drop(columns=["awareness", "consideration", "decision_making", "purchase", "service", "loyalty",
                             "ambassador"])  # All columns before targets

        Y = {
            "Awareness": df["awareness"],
            "Consideration": df["consideration"],
            "Decision-Making": df["decision_making"],
            "Purchase": df["purchase"],
            "Service": df["service"],
            "Loyalty": df["loyalty"],
            "Ambassador": df["ambassador"]
        }

        X = X.values.reshape(X.shape[0], 1, X.shape[1])

        for stage in journey_stages:
            num_touchpoints = len(custJourneyData[stage])
            model = Sequential()
            model.add(LSTM(units=50, activation='relu', input_shape=(X.shape[1], X.shape[2])))
            model.add(Dense(num_touchpoints, activation='softmax', name=f"stage_{stage}"))

            model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
            model.fit(X, Y[stage], epochs=50, batch_size=32)

            models[stage] = model

    @staticmethod
    def handleUnseenData(df_new, label_encoders):
        for column in df_new.columns:
            if column in label_encoders:
                le = label_encoders[column]
                # Identify new classes not present in the original encoder
                new_classes = set(df_new[column].astype(str)) - set(le.classes_)
                if new_classes:
                    # Assign the next available encoding to unseen classes
                    current_max = len(le.classes_)
                    new_class_map = {cls: current_max + idx for idx, cls in enumerate(new_classes, start=1)}
                    le.classes_ = np.append(le.classes_, list(new_classes))

                    # Transform existing data and map new unseen data
                    df_new[column] = df_new[column].apply(
                        lambda x: le.transform([x])[0] if x in le.classes_ else new_class_map[x]
                    )
                else:
                    df_new[column] = le.transform(df_new[column])
            else:

                le = LabelEncoder()
                le.fit(df_new[column].astype(str))
                label_encoders[column] = le
                df_new[column] = le.transform(df_new[column])


        return df_new

    # ------------
    # Predicting
    # ------------
    @staticmethod
    def get_segmentation(micro_object, models, encoders):

        df_test = pd.DataFrame([{
            # Micro Segmentation
            "age": micro_object.age,
            "gender": micro_object.gender,
            "education_level": micro_object.education_level,
            "technology_used": micro_object.technology_used,
            "job_title": micro_object.job_title,
            "experience_level": micro_object.experience_level,
            "functional_field": micro_object.functional_field,
            "decision_making_role": micro_object.decision_making_role,
            "work_environment": micro_object.work_environment,
            "professional_network": micro_object.professional_network,
            "risk_tolerance": micro_object.risk_tolerance,
            "decision_making_style": micro_object.decision_making_style,
            "motivations": micro_object.motivations,
            "personality_traits": micro_object.personality_traits,
            "pain_points": micro_object.pain_points,
            "kpis": micro_object.kpis,
            "challenges": micro_object.challenges,
            "goals": micro_object.goals
        }])


        # Handle unseen data and encode
        df_test_encoded = CustomerJourneyModel.handleUnseenData(df_test.copy(), encoders)

        # Reshape for model input
        X_test = df_test_encoded.values.reshape(df_test_encoded.shape[0], 1, df_test_encoded.shape[1])

        best_predictions = {}
        # Predict
        for stage in journey_stages:

            stage_model = models[stage]
            prediction = stage_model.predict(X_test)[0]

            # Sort predictions (probabilities) from best to worst
            sorted_indices = np.argsort(prediction)[::-1]
            sorted_touchpoints = [custJourneyData[stage][i] for i in sorted_indices]

            # Create a dictionary of sorted predictions with their probabilities
            sorted_predictions = {sorted_touchpoints[i]: prediction[sorted_indices[i]] for i in
                                  range(len(sorted_touchpoints))}

            best_predictions[stage] = sorted_touchpoints[0]


            for i in range(len(sorted_touchpoints)):
                touchpoint = sorted_touchpoints[i]
                prob = prediction[sorted_indices[i]]


        customer_journey = CustomerJourney(
            micro_segmentation=micro_object,
            awareness=best_predictions["Awareness"],
            consideration=best_predictions["Consideration"],
            decision_making=best_predictions["Decision-Making"],
            purchase=best_predictions["Purchase"],
            service=best_predictions["Service"],
            loyalty=best_predictions["Loyalty"],
            ambassador=best_predictions["Ambassador"]
        )
        return customer_journey

    @staticmethod
    def save_model(filepath):

        os.makedirs(filepath, exist_ok=True)
        for stage, model in models.items():
            model_path = os.path.join(filepath, f"{stage}_model.h5")
            model.save(model_path)

        encoders_path = os.path.join(filepath, "label_encoders.joblib")
        joblib.dump(label_encoders, encoders_path)


    @staticmethod
    def load_model(filepath):

        models = {}
        for stage in journey_stages:
            model_path = os.path.join(filepath, f"{stage}_model.h5")
            if os.path.exists(model_path):
                models[stage] = tf.keras.models.load_model(model_path)
            else:
                raise FileNotFoundError(f"Model file not found for stage: {stage}")

        encoders_path = os.path.join(filepath, "label_encoders.joblib")
        if os.path.exists(encoders_path):
            loaded_label_encoders = joblib.load(encoders_path)
        else:
            raise FileNotFoundError("Label encoders file not found")

        return models, loaded_label_encoders

    @staticmethod
    def load_and_predict(filepath, micro_object):

        models, encoders = CustomerJourneyModel.load_model(filepath)

        customer_journey = CustomerJourneyModel.get_segmentation(micro_object, models, encoders)

        return customer_journey

    def setup(filepath):
        with app.app_context():
            df_train = CustomerJourneyModel.fetch_data()
            df_encoded = CustomerJourneyModel.encoding(df_train)
            model = CustomerJourneyModel()
            models = model.train_model(df_encoded)

            CustomerJourneyModel.save_model(filepath=filepath)

        # --------------
        # Testing
        # --------------


def test_journey():
    filepath = "models/customerjourneyModel.joblib"
    CustomerJourneyModel.setup(filepath=filepath)

    input_object = InputFields(
        industry="Finance and Insurance",
        organization_size="11-50 employees",
        annual_revenue="€1 million - €10 million",
        location=["North America"],
        geographical_focus="Global",
        strategic_positioning=["Cost Leader", "Innovation Leader"]
    )

    macro_object = MacroSegmentation(

        input_fields=input_object,
        # demographic segment
        industry='Software Development',
        organization_size='501-5000 employees',
        annual_revenue='€50 million - €100 million',

        # geographic segments
        operational_regions='Global presence',
        market_density='Urban',

        # behavioral segmentation
        purchasing_frequency='Occasional buyers',
        purchasing_volume='Medium volume: €50,000 - €500,000 per year',
        technology_adoption='Early Adopters',
        usage_engagement_rate='Heavy users',

        # firmographic segmentation
        ownership_structure='Private',
        growth_stage='Startup',

        # DMU Segmentation allowed attributes
        influence_structure='Owner/Founder led'
    )

    micro_object = MicroSegmentation(
        macro_segmentation=macro_object,

        # personal background
        age='60+',
        gender='Male',
        education_level='High School',
        technology_used='Low',

        # professional background
        job_title='Senior-level',
        experience_level='Entry-Level: 0-3 years',
        functional_field='Technology & IT',
        decision_making_role='Primary decision-maker',
        work_environment='Remote',
        professional_network='Time Management',

        # Psychological Profile
        risk_tolerance='Risk-Averse',
        decision_making_style='Peer-Influenced',
        motivations='Efficiency',
        personality_traits='Collaborative vs. Independent',
        pain_points='Team/Resource Limitations',

        # KPIs
        kpis='Human Resources KPI',

        # Challenges
        challenges='General Business',

        # Goals
        goals='Marketing'
    )

    predictions = CustomerJourneyModel.load_and_predict(filepath, micro_object)

