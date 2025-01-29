import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import cdist
from sklearn.preprocessing import StandardScaler
from flask import Flask
from backend.objects.inputObj import InputFields
from backend.objects.macroObj import MacroSegmentation
from backend.database import db
import joblib
import os

# Flask App Setup
# Initializes the Flask app and database configuration
app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/miloudrapers/Desktop/Project 3.1/vesper_project/instance/vesper.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


class MacroClusteringModel:
    def __init__(self):
        self.scaler = None
        self.combined_df_encoded = None
        self.cluster_labels = None
        self.input_macro_map = None

    @staticmethod
    def fetch_data():
        with app.app_context():
            inputs = InputFields.query.all()
            macros = MacroSegmentation.query.all()

            input_data = [
                [
                    i.industry,
                    i.organization_size,
                    i.annual_revenue,
                    ','.join(i.location),
                    i.geographical_focus,
                    ','.join(i.strategic_positioning),
                ]
                for i in inputs
            ]

            macro_data = [
                [
                    m.industry,
                    m.organization_size,
                    m.annual_revenue,
                    m.operational_regions,
                    m.market_density,
                    m.purchasing_frequency,
                    m.purchasing_volume,
                    m.technology_adoption,
                    m.usage_engagement_rate,
                    m.ownership_structure,
                    m.growth_stage,
                    m.influence_structure,
                ]
                for m in macros
            ]

            return pd.DataFrame(input_data), pd.DataFrame(macro_data)

    # Preprocess Data
    @staticmethod
    def preprocess_data(input_df, macro_df):
        combined_df = pd.concat([input_df, macro_df], axis=1).dropna()

        # Encode categorical variables
        combined_df_encoded = pd.get_dummies(combined_df)

        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(combined_df_encoded)

        return scaled_data, scaler, combined_df_encoded

    def generate_model(self, input_df, macro_df):
        scaled_data, self.scaler, self.combined_df_encoded = self.preprocess_data(input_df, macro_df)

        self.cluster_labels = fcluster(linkage(scaled_data, method='ward'), t=5, criterion='maxclust')

        self.input_macro_map = {}
        for cluster in np.unique(self.cluster_labels):
            cluster_inputs = input_df[self.cluster_labels == cluster]

            macro_objects = macro_df.iloc[cluster_inputs.index]

            self.input_macro_map[cluster] = macro_objects

    def convert_input_to_vector(self, input_obj):
        input_data = {
            "industry": input_obj.industry,
            "organization_size": input_obj.organization_size,
            "annual_revenue": input_obj.annual_revenue,
            "location": ','.join(input_obj.location),
            "geographical_focus": input_obj.geographical_focus,
            "strategic_positioning": ','.join(input_obj.strategic_positioning),
        }
        input_df = pd.DataFrame([input_data])
        input_encoded = pd.get_dummies(input_df)

        input_encoded = input_encoded.reindex(columns=self.combined_df_encoded.columns, fill_value=0)

        return input_encoded.values[0]

    # Predict Top 3 Macro Features for InputFields Object
    def predict_top_macro_features_for_input(self, input_obj):

        new_input_vector = self.convert_input_to_vector(input_obj)

        new_input_scaled = self.scaler.transform([new_input_vector])

        distances = cdist(new_input_scaled, self.combined_df_encoded.values)
        sorted_indices = np.argsort(distances[0])[:3]
        top_clusters = [self.cluster_labels[i] for i in sorted_indices]

        top_macro = [self.input_macro_map.get(cluster, None) for cluster in top_clusters]

        top_macro_objects = []

        for idx, cluster in enumerate(top_macro):


            macro = MacroSegmentation(
                input_fields=input_obj,
                industry=str(cluster.iloc[0, 0]),
                organization_size=str(cluster.iloc[0, 1]),
                annual_revenue=str(cluster.iloc[0, 2]),
                operational_regions=str(cluster.iloc[0, 3]),
                market_density=str(cluster.iloc[0, 4]),
                purchasing_frequency=str(cluster.iloc[0, 5]),
                purchasing_volume=str(cluster.iloc[0, 6]),
                technology_adoption=str(cluster.iloc[0, 7]),
                usage_engagement_rate=str(cluster.iloc[0, 8]),
                ownership_structure=str(cluster.iloc[0, 9]),
                growth_stage=str(cluster.iloc[0, 10]),
                influence_structure=str(cluster.iloc[0, 11]))

            top_macro_objects.append(macro)

        return top_macro_objects

    def save_model(self, filepath):
        model_data = {
            "scaler": self.scaler,
            "combined_df_encoded": self.combined_df_encoded,
            "cluster_labels": self.cluster_labels,
            "input_macro_map": self.input_macro_map,
        }
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(model_data, filepath)


    @staticmethod
    def load_model(filepath):
        model_data = joblib.load(filepath)
        model = MacroClusteringModel()
        model.scaler = model_data["scaler"]
        model.combined_df_encoded = model_data["combined_df_encoded"]
        model.cluster_labels = model_data["cluster_labels"]
        model.input_macro_map = model_data["input_macro_map"]
        return model

    def load_and_predict(filepath, new_input):
        model = MacroClusteringModel.load_model(filepath)
        top_clusters = model.predict_top_macro_features_for_input(new_input)
        return top_clusters

    def setup(filepath):
        with app.app_context():
            input_df, macro_df = MacroClusteringModel.fetch_data()

            model = MacroClusteringModel()
            model.generate_model(input_df, macro_df)
            model.save_model(filepath=filepath)


# Testing Functionality
# Demonstrates the full workflow:
# 1. Generating and storing the model
# 2. Predicting macro objects for a new input
def test_clustering():
    filepath = "models/macroModel.joblib"
    MacroClusteringModel.setup(filepath=filepath)

    # Example new input as InputFields object
    new_input = InputFields(
        industry="Finance and Insurance",
        organization_size="11-50 employees",
        annual_revenue="€1 million - €10 million",
        location=["North America"],
        geographical_focus="Global",
        strategic_positioning=["Cost Leader", "Innovation Leader"]
    )

    top_clusters = MacroClusteringModel.load_and_predict(filepath, new_input)


