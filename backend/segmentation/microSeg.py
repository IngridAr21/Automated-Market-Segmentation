import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import cdist
from sklearn.preprocessing import StandardScaler
from flask import Flask
from backend.objects.inputObj import InputFields
from backend.objects.macroObj import MacroSegmentation
from backend.objects.microObj import MicroSegmentation
from backend.database import db
import joblib
import os

# Flask App Setup
app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/miloudrapers/Desktop/Project 3.1/vesper_project/instance/vesper.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


class MicroClusteringModel:
    def __init__(self):
        self.scaler = None
        self.combined_df_encoded = None
        self.cluster_labels = None
        self.macro_micro_map = None

    @staticmethod
    def fetch_data():
        with app.app_context():
            macros = MacroSegmentation.query.all()
            micros = MicroSegmentation.query.all()

            macro_data = [
                [
                    m.id,
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

            micro_data = [
                [
                    mic.macro_segmentation_id,
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

            macro_columns = [
                "id", "industry", "organization_size", "annual_revenue", "operational_regions",
                "market_density", "purchasing_frequency", "purchasing_volume", "technology_adoption",
                "usage_engagement_rate", "ownership_structure", "growth_stage", "influence_structure"
            ]

            micro_columns = [
                "macro_segmentation_id", "age", "gender", "education_level", "technology_used",
                "job_title", "experience_level", "functional_field", "decision_making_role",
                "work_environment", "professional_network", "risk_tolerance", "decision_making_style",
                "motivations", "personality_traits", "pain_points", "kpis", "challenges", "goals"
            ]

            return pd.DataFrame(macro_data, columns=macro_columns), pd.DataFrame(micro_data, columns=micro_columns)

    @staticmethod
    def preprocess_data(macro_df, micro_df):
        combined_df = pd.concat([macro_df, micro_df], axis=1).dropna()

        combined_df_encoded = pd.get_dummies(combined_df)

        boolean_columns = combined_df_encoded.select_dtypes(include=['bool']).columns
        combined_df_encoded[boolean_columns] = combined_df_encoded[boolean_columns].astype(int)

        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(combined_df_encoded)

        return scaled_data, scaler, combined_df_encoded

    def generate_model(self, macro_df, micro_df):
        scaled_data, self.scaler, self.combined_df_encoded = self.preprocess_data(macro_df, micro_df)

        self.cluster_labels = fcluster(linkage(scaled_data, method='ward'), t=5, criterion='maxclust')

        self.macro_micro_map = {}
        for cluster in np.unique(self.cluster_labels):
            cluster_macros = macro_df[self.cluster_labels == cluster]

            micro_objects = micro_df[micro_df["macro_segmentation_id"].isin(cluster_macros["id"])]

            self.macro_micro_map[cluster] = micro_objects

    def convert_macro_to_vector(self, macro_obj):
        macro_data = {
            "industry": macro_obj.industry,
            "organization_size": macro_obj.organization_size,
            "annual_revenue": macro_obj.annual_revenue,
            "operational_regions": macro_obj.operational_regions,
            "market_density": macro_obj.market_density,
            "purchasing_frequency": macro_obj.purchasing_frequency,
            "purchasing_volume": macro_obj.purchasing_volume,
            "technology_adoption": macro_obj.technology_adoption,
            "usage_engagement_rate": macro_obj.usage_engagement_rate,
            "ownership_structure": macro_obj.ownership_structure,
            "growth_stage": macro_obj.growth_stage,
            "influence_structure": macro_obj.influence_structure,
        }
        macro_df = pd.DataFrame([macro_data])
        macro_encoded = pd.get_dummies(macro_df)

        macro_encoded = macro_encoded.reindex(columns=self.combined_df_encoded.columns, fill_value=0)

        return macro_encoded.astype(float).values[0]

    def predict_top_micro_features_for_macro(self, macro_obj):

        new_macro_vector = self.convert_macro_to_vector(macro_obj)

        new_macro_scaled = self.scaler.transform([new_macro_vector])

        distances = cdist(new_macro_scaled, self.combined_df_encoded.values)
        sorted_indices = np.argsort(distances[0])[:3]  # Get top 3 closest clusters
        top_clusters = [self.cluster_labels[i] for i in sorted_indices]

        top_micro = [self.macro_micro_map.get(cluster, None) for cluster in top_clusters]

        top_micro_objects = []
        for idx, cluster in enumerate(top_micro):
            micro = MicroSegmentation(
                macro_segmentation=macro_obj,
                age=str(cluster.iloc[0, 1]),
                gender=str(cluster.iloc[0, 2]),
                education_level=str(cluster.iloc[0, 3]),
                technology_used=str(cluster.iloc[0, 4]),
                job_title=str(cluster.iloc[0, 5]),
                experience_level=str(cluster.iloc[0, 6]),
                functional_field=str(cluster.iloc[0, 7]),
                decision_making_role=str(cluster.iloc[0, 8]),
                work_environment=str(cluster.iloc[0, 9]),
                professional_network=str(cluster.iloc[0, 10]),
                risk_tolerance=str(cluster.iloc[0, 11]),
                decision_making_style=str(cluster.iloc[0, 12]),
                motivations=str(cluster.iloc[0, 13]),
                personality_traits=str(cluster.iloc[0, 14]),
                pain_points=str(cluster.iloc[0, 15]),
                kpis=str(cluster.iloc[0, 16]),
                challenges=str(cluster.iloc[0, 17]),
                goals=str(cluster.iloc[0, 18])
            )
            top_micro_objects.append(micro)

        return top_micro_objects

    def save_model(self, filepath):
        model_data = {
            "scaler": self.scaler,
            "combined_df_encoded": self.combined_df_encoded,
            "cluster_labels": self.cluster_labels,
            "macro_micro_map": self.macro_micro_map,
        }
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(model_data, filepath)

    @staticmethod
    def load_model(filepath):
        model_data = joblib.load(filepath)
        model = MicroClusteringModel()
        model.scaler = model_data["scaler"]
        model.combined_df_encoded = model_data["combined_df_encoded"]
        model.cluster_labels = model_data["cluster_labels"]
        model.macro_micro_map = model_data["macro_micro_map"]
        return model

    @staticmethod
    def load_and_predict(filepath, new_macro):
        model = MicroClusteringModel.load_model(filepath)
        return model.predict_top_micro_features_for_macro(new_macro)

    def setup(filepath):
        with app.app_context():
            macro_df, micro_df = MicroClusteringModel.fetch_data()
            model = MicroClusteringModel()
            model.generate_model(macro_df, micro_df)
            model.save_model(filepath)


# Testing Functionality
# Demonstrates the full workflow:
# 1. Generating and storing the model
# 2. Predicting micro objects for a macro input
def test_clustering():
    filepath = "models/microModel.joblib"
    MicroClusteringModel.setup(filepath=filepath)

    # Example new input as MacroSegmentation object
    new_input = InputFields(
        industry="Finance and Insurance",
        organization_size="11-50 employees",
        annual_revenue="€1 million - €10 million",
        location=["North America"],
        geographical_focus="Global",
        strategic_positioning=["Cost Leader", "Innovation Leader"]
    )

    new_macro = MacroSegmentation(
        input_fields=new_input,
        industry="Finance and Insurance",
        organization_size="11-50 employees",
        annual_revenue="€1 million - €10 million",
        operational_regions="Global presence",
        market_density="Urban",
        purchasing_frequency="Occasional buyers",
        purchasing_volume="Medium volume: €50,000 - €500,000 per year",
        technology_adoption="Early Adopters",
        usage_engagement_rate="Medium users",
        ownership_structure="Private",
        growth_stage="Growth Stage",
        influence_structure="CEO/Executive Driven"
    )

    # Predict top micro objects for the new macro input
    top_micro_objects = MicroClusteringModel.load_and_predict(filepath, new_macro)



if __name__ == "__main__":
    test_clustering()
