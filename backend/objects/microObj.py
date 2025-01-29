from random import choices, sample
import random
from sqlalchemy.orm import relationship
from backend.database import db


class MicroSegmentation(db.Model):
    __tablename__ = 'micro_segmentation'
    id = db.Column(db.Integer, primary_key=True)
    macro_segmentation_id = db.Column(db.Integer, db.ForeignKey('macro_segmentation.id'), nullable=False)
    macro_segmentation = relationship('MacroSegmentation', backref='micro_segments')  # Define relationship
    age = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    education_level = db.Column(db.String(50), nullable=False)
    technology_used = db.Column(db.String(255), nullable=False)
    job_title = db.Column(db.String(255), nullable=False)
    experience_level = db.Column(db.String(50), nullable=False)
    functional_field = db.Column(db.String(255), nullable=False)
    decision_making_role = db.Column(db.String(255), nullable=False)
    work_environment = db.Column(db.String(255), nullable=False)
    professional_network = db.Column(db.String(255), nullable=False)
    risk_tolerance = db.Column(db.String(255), nullable=False)
    decision_making_style = db.Column(db.String(255), nullable=False)
    motivations = db.Column(db.Text, nullable=False)
    personality_traits = db.Column(db.Text, nullable=False)
    pain_points = db.Column(db.Text, nullable=False)
    kpis = db.Column(db.Text, nullable=False)
    challenges = db.Column(db.Text, nullable=False)
    goals = db.Column(db.Text, nullable=False)

    allowed_age = ['18-25', '26-35', '36-45', '45-60', '60+', None]
    allowed_gender = ['Male', 'Female', 'Non-binary', None]
    allowed_education_level = ['High school', 'Bachelor\'s degree', 'Master\'s degree', 'Doctorate degree', None]
    allowed_tech_use = ['Low', 'Medium', 'High', None]

    allowed_job_title = ['Entry-Level', 'Mid-Level', 'Senior-Level', 'C-Suite', None]
    allowed_experience_level = ['Entry-Level: 0-3 years', 'Mid-Level: 4-10 years', 'Senior-Level: 10+ years', None]
    allowed_functional_field = ['Finance & Accounting', 'Operations', 'Marketing & Communication', 'Sales',
                                'Technology & IT',
                                'Product Management', 'Human Resources', 'Legal & Compliance', 'Customer Service',
                                'R&D', 'Procurement',
                                'Manufacturing', 'Logistics', None]
    allowed_decision_making_role = ['Primary decision-maker', 'Influencer', 'Recommender', None]
    allowed_work_enviroment = ['Office-Based', 'Remote', 'Hybrid', 'On-site', None]
    allowed_select_experience_levels = {
        "Entry-Level": {"years": (0, 3), "titles": ["Analyst", "Associate"]},
        "Mid-Level": {"years": (4, 10), "titles": ["Manager", "Supervisor"]},
        "Senior-Level": {"years": (10, None), "titles": ["Director", "VP", "Executive"]},
        "C-Suite": {"years": (15, None), "titles": ["CEO", "CFO", "COO", "CTO", "CMO"]}
    }
    allowed_industry_work_environment_weights = {
        "Agriculture, Forestry, Fishing and Hunting": {"Field-Based": 0.8, "Hybrid": 0.15, "Remote": 0.05},
        "Mining, Quarrying, and Oil and Gas Extraction": {"Field-Based": 0.85, "Office-Based": 0.1, "Remote": 0.05},
        "Utilities": {"Office-Based": 0.5, "Field-Based": 0.4, "Remote": 0.1},
        "Construction": {"Field-Based": 0.7, "Hybrid": 0.2, "Office-Based": 0.1},
        "Manufacturing": {"Office-Based": 0.4, "Field-Based": 0.4, "Hybrid": 0.15, "Remote": 0.05},
        "Wholesale Trade": {"Office-Based": 0.6, "Hybrid": 0.3, "Remote": 0.1},
        "Retail Trade": {"Office-Based": 0.65, "Field-Based": 0.2, "Remote": 0.15},
        "Transportation and Warehousing": {"Field-Based": 0.6, "Office-Based": 0.3, "Remote": 0.1},
        "Information": {"Remote": 0.5, "Hybrid": 0.3, "Office-Based": 0.2},
        "Finance and Insurance": {"Office-Based": 0.6, "Hybrid": 0.3, "Remote": 0.1},
        "Real Estate and Rental and Leasing": {"Office-Based": 0.5, "Hybrid": 0.3, "Field-Based": 0.2},
        "Professional, Scientific, and Technical Services": {"Office-Based": 0.5, "Remote": 0.3, "Hybrid": 0.2},
        "Management of Companies and Enterprises": {"Office-Based": 0.6, "Remote": 0.2, "Hybrid": 0.2},
        "Administrative and Support and Waste Management and Remediation Services": {"Office-Based": 0.5, "Hybrid": 0.3,
                                                                                     "Remote": 0.2},
        "Educational Services": {"On-Site": 0.6, "Hybrid": 0.3, "Remote": 0.1},
        "Health Care and Social Assistance": {"On-Site": 0.7, "Hybrid": 0.2, "Remote": 0.1},
        "Arts, Entertainment, and Recreation": {"On-Site": 0.7, "Hybrid": 0.2, "Remote": 0.1},
        "Accommodation and Food Services": {"On-Site": 0.75, "Hybrid": 0.15, "Remote": 0.1},
        "Other Services (except Public Administration)": {"Office-Based": 0.5, "Hybrid": 0.3, "Remote": 0.2},
        "Public Administration": {"Office-Based": 0.6, "Hybrid": 0.3, "Remote": 0.1},
        "Telecommunications": {"Remote": 0.5, "Hybrid": 0.3, "Office-Based": 0.2},
        "Aerospace and Defense": {"Office-Based": 0.6, "Field-Based": 0.2, "Remote": 0.2},
        "Biotechnology": {"Office-Based": 0.5, "Laboratory-Based": 0.4, "Remote": 0.1},
        "Chemicals": {"Office-Based": 0.5, "Field-Based": 0.3, "Remote": 0.2},
        "Consumer Goods": {"Office-Based": 0.6, "Hybrid": 0.3, "Remote": 0.1},
        "E-commerce": {"Remote": 0.5, "Hybrid": 0.3, "Office-Based": 0.2},
        "Environmental Services": {"Field-Based": 0.6, "Hybrid": 0.3, "Remote": 0.1},
        "Government": {"Office-Based": 0.7, "Hybrid": 0.2, "Remote": 0.1},
        "Legal Services": {"Office-Based": 0.7, "Remote": 0.2, "Hybrid": 0.1},
        "Media and Entertainment": {"Hybrid": 0.4, "Office-Based": 0.4, "Remote": 0.2},
        "Pharmaceuticals": {"Office-Based": 0.5, "Laboratory-Based": 0.3, "Hybrid": 0.2},
        "Renewable Energy": {"Field-Based": 0.5, "Office-Based": 0.3, "Remote": 0.2},
        "Software Development": {"Remote": 0.6, "Hybrid": 0.3, "Office-Based": 0.1},
        "Tourism and Travel": {"On-Site": 0.6, "Hybrid": 0.3, "Remote": 0.1},
        "Automotive": {"Office-Based": 0.4, "Field-Based": 0.4, "Hybrid": 0.2},
        "Food and Beverage": {"On-Site": 0.7, "Office-Based": 0.2, "Hybrid": 0.1},
        "Hospitality": {"On-Site": 0.7, "Hybrid": 0.2, "Remote": 0.1},
        "Insurance": {"Office-Based": 0.6, "Remote": 0.3, "Hybrid": 0.1},
        "Logistics and Supply Chain": {"Field-Based": 0.5, "Office-Based": 0.3, "Remote": 0.2},
        "Nonprofit": {"Office-Based": 0.6, "Hybrid": 0.3, "Remote": 0.1},
        "Printing and Publishing": {"Office-Based": 0.6, "Hybrid": 0.3, "Remote": 0.1},
        "Real Estate Development": {"Field-Based": 0.5, "Office-Based": 0.4, "Hybrid": 0.1},
        "Retail and Consumer Goods": {"Office-Based": 0.6, "Hybrid": 0.3, "Remote": 0.1},
        "Shipping and Maritime": {"Field-Based": 0.7, "Office-Based": 0.2, "Remote": 0.1},
        "Sports and Recreation": {"On-Site": 0.8, "Hybrid": 0.15, "Remote": 0.05},
        "Textiles and Apparel": {"Office-Based": 0.5, "Hybrid": 0.3, "Remote": 0.2},
        "Venture Capital and Private Equity": {"Office-Based": 0.7, "Hybrid": 0.2, "Remote": 0.1},
        "Waste Management": {"Field-Based": 0.6, "Office-Based": 0.3, "Remote": 0.1},
        "Wood Products": {"Field-Based": 0.6, "Office-Based": 0.3, "Remote": 0.1},
        "Zoological and Botanical Gardens": {"On-Site": 0.8, "Hybrid": 0.2},
    }

    allowed_risk_tolerance = ['Risk-Averse', 'Moderate Risk-Taker', 'High Risk-Taker', None]
    allowed_decision_making_style = ['Fast', 'Cautious', 'Data-Driven', 'Intuitive', 'Peer-Influenced', None]
    allowed_motivations = ['Efficiency', 'Prestige', 'Innovation', 'Stability', 'Customer-Centricity', None]
    allowed_personality_traits = ['Extroverted vs. Introverted', 'Analytical vs. Creative',
                                  'Detail-Oriented vs. Big-Picture Thinker', 'Collaborative vs. Independent', None]
    allowed_pain_points = ['Time Management', 'Budget Constraints', 'Team/Resource Limitations',
                           'Complex Decision-Making Process', None]

    allowed_kpis = {
        'Business KPIs': {
            'Revenue Growth', 'Profit Margins', 'Customer Acquisition Cost (CAC)', 'Customer Lifetime Value (CLTV)',
            'Sales Growth', 'Customer Retention Rate', 'Churn Rate', 'Return on Investment (ROI)',
            'Cost of Goods Sold (COGS)', 'Market Share Growth', 'Website Traffic', 'Net Promoter Score (NPS)',
            'Operational Efficiency', 'Employee Retention Rate', None
        },
        'Marketing KPIs': [
            'Lead Conversion Rate', 'Click-Through Rate (CTR)', 'Cost Per Lead (CPL)',
            'Return on Ad Spend (ROAS)', 'Social Media Engagement', None
        ],
        'Product & Customer Service KPIs': [
            'First Response Time', 'Customer Satisfaction Score (CSAT)', 'Ticket Resolution Time',
            'Product Adoption Rate',
            'Service Level Agreement (SLA) Compliance', None
        ],
        'Human Resources KPIs': [
            'Employee Engagement Score', 'Time to Fill', 'Training Completion Rate', 'Diversity & Inclusion Metrics',
            None
        ]
    }

    allowed_challenges = {
        'General Business Challenges': [
            'Budget Constraints', 'Market Saturation', 'Pricing Pressure', 'Regulatory Compliance',
            'Supply Chain Disruptions', 'Scaling Operations', 'Economic Downturns', 'Industry Trends',
            'Maintaining Profitability', 'Talent Retention', 'Data Privacy', 'Resource Constraints',
            'Customer Expectations', None
        ],
        'Marketing Challenges': [
            'Lead Quality', 'Brand Awareness', 'Customer Segmentation', 'Attribution', 'Personalization', None
        ],
        'Sales Challenges': [
            'Long Sales Cycles', 'Low Close Rates', 'Objections on Price', 'Cold Outreach Ineffectiveness',
            'Competitive Differentiation', None
        ],
        'Operation Challenges': [
            'Legacy Systems', 'Manual Processes', 'Data Overload', 'Cross-Team Communication', 'Change Resistance', None
        ],
        'Product Challenges': [
            'Product Bugs', 'High Support Volume', 'Feature Requests', 'Churn', 'Self-Service Options', None
        ]
    }

    allowed_goals = {
        'General Business Goals': [
            'Revenue Growth', 'Market Expansion', 'Profitability Improvement', 'Digital Transformation',
            'Sustainability Improvement', 'Brand Loyalty Improvement', 'Diversification', None
        ],
        'Sales Goals': [
            'Increase Lead Generation', 'Shorten Sales Cycles', 'Improve Lead-to-Customer Conversion',
            'Expand into Enterprise Accounts', 'Develop Sales Enablement', 'Boost Sales Team Productivity', None
        ],
        'Marketing Goals': [
            'Improve Brand Awareness', 'Increase Web Traffic', 'Increase Content Engagement',
            'Increase Social Media Presence', 'Launch New Products', 'Increase Event Attendance', None
        ],
        'Customer Service Goals': [
            'Improve First-Response Time', 'Increase Customer Satisfaction', 'Reduce Churn Rate',
            'Expand Self-Service Options', 'Upsell Existing Customers', None
        ],
        'Operations Goals': [
            'Optimize Efficiency', 'Implement Automation', 'Improve Supply Chain', 'Reduce Operating Costs',
            'Increase Data Visibility', None
        ]
    }

    def __init__(self, macro_segmentation, age, gender, education_level, technology_used,
                 job_title, experience_level, functional_field, decision_making_role, work_environment,
                 professional_network,
                 risk_tolerance, decision_making_style, motivations, personality_traits, pain_points,
                 kpis, challenges, goals
                 ):

        self.macro_segmentation = macro_segmentation

        self.age = age
        self.gender = gender
        self.education_level = education_level
        self.technology_used = technology_used

        self.job_title = job_title
        self.experience_level = experience_level
        self.functional_field = functional_field
        self.decision_making_role = decision_making_role
        self.work_environment = work_environment
        self.professional_network = professional_network

        self.risk_tolerance = risk_tolerance
        self.decision_making_style = decision_making_style
        self.motivations = motivations
        self.personality_traits = personality_traits
        self.pain_points = pain_points

        self.kpis = kpis

        self.challenges = challenges

        self.goals = goals

    def generate_micro(macro):

        macro_segmentation = macro

        work_environment = MicroSegmentation.select_work_environment(macro.get_industry())

        age = choices(MicroSegmentation.allowed_age, weights=[0.05, 0.25, 0.25, 0.25, 0.2, 0.0])[0]
        gender = choices(MicroSegmentation.allowed_gender, weights=[0.59, 0.40, 0.01, 0.0])[0]
        education_level = choices(MicroSegmentation.allowed_education_level, weights=[0.3, 0.5, 0.15, 0.05, 0.0])[0]

        # Profesional background
        experience_level = MicroSegmentation.select_experience_level_based_on_age(age)
        job_title = MicroSegmentation.select_job_title_based_on_industry(macro.get_industry(), experience_level)
        functional_field = MicroSegmentation.select_functional_field(job_title)
        decision_making_role = MicroSegmentation.select_decision_making_role(macro.get_influence_structure())
        professional_network = MicroSegmentation.select_professional_network(age, job_title, education_level)

        technology_used = MicroSegmentation.select_technology_used(education_level, functional_field, work_environment)

        pain_points = choices(MicroSegmentation.allowed_pain_points, weights=[0.3, 0.25, 0.2, 0.25, 0])[0]
        risk_tolerance = MicroSegmentation.select_risk_tolerance(age, gender)
        personality_traits = MicroSegmentation.select_personality_traits(risk_tolerance)
        motivations = MicroSegmentation.select_motivations(personality_traits)
        decision_making_style = MicroSegmentation.select_decision_making_style(macro.get_industry(), age, motivations,
                                                                               pain_points)

        kpis = MicroSegmentation.select_kpis(job_title)
        challenges = MicroSegmentation.select_goals(job_title, macro.get_industry())
        goals = MicroSegmentation.select_goals(job_title, macro.get_industry())

        return MicroSegmentation(
            macro_segmentation=macro_segmentation,
            age=age,
            gender=gender,
            education_level=education_level,
            technology_used=technology_used,

            job_title=job_title,
            experience_level=experience_level,
            functional_field=functional_field,
            decision_making_role=decision_making_role,
            work_environment=work_environment,
            professional_network=professional_network,

            risk_tolerance=risk_tolerance,
            decision_making_style=decision_making_style,
            motivations=motivations,
            personality_traits=personality_traits,
            pain_points=pain_points,

            kpis=kpis,

            challenges=challenges,

            goals=goals,

        )

    def weighted_choice(options):

        weights = [1 if option is not None else 0 for option in options]
        return choices(options, weights=weights, k=1)[0]

    def weighted_sample(options, k):

        weights = [1 if option is not None else 0 for option in options]
        return sample(choices(options, weights=weights, k=len(options)), k)

    def select_goals(job_title, industry_field):

        if job_title == "C-Suite":
            return choices(
                ["Market Expansion", "Profitability Improvement", "Sustainability Improvement",
                 "Brand Loyalty Improvement"],
                weights=[0.4, 0.3, 0.2, 0.1]
            )[0]
        elif job_title == "Senior-Level":
            return choices(
                ["Optimize Efficiency", "Improve Supply Chain", "Reduce Operating Costs", "Increase Data Visibility"],
                weights=[0.4, 0.3, 0.2, 0.1]
            )[0]
        elif industry_field in ["Sales", "Marketing & Communication"]:
            return choices(
                ["Increase Lead Generation", "Improve Brand Awareness", "Boost Social Media Presence",
                 "Launch New Products"],
                weights=[0.3, 0.3, 0.2, 0.2]
            )[0]
        elif industry_field in ["Technology & IT", "R&D"]:
            return choices(
                ["Digital Transformation", "Increase Data Visibility", "Implement Automation", "Develop New Products"],
                weights=[0.4, 0.3, 0.2, 0.1]
            )[0]
        else:
            return choices(
                ["Revenue Growth", "Employee Engagement", "Customer Satisfaction", "Sustainability Improvement"],
                weights=[0.3, 0.3, 0.2, 0.2]
            )[0]

    def select_kpis(job_title):
        if job_title == "C-Suite":
            return choices(
                ["Revenue Growth", "Profit Margins", "Customer Acquisition Cost (CAC)", "Market Share Growth"],
                weights=[0.4, 0.3, 0.2, 0.1]
            )[0]
        elif job_title == "Senior-Level":
            return choices(
                ["Operational Efficiency", "Customer Retention Rate", "Sales Growth", "Employee Retention Rate"],
                weights=[0.3, 0.3, 0.2, 0.2]
            )[0]
        elif job_title == "Mid-Level":
            return choices(
                ["Cost of Goods Sold (COGS)", "Lead Conversion Rate", "Website Traffic", "Social Media Engagement"],
                weights=[0.3, 0.3, 0.2, 0.2]
            )[0]
        else:
            return choices(
                ["Revenue Growth", "Operational Efficiency", "Customer Retention Rate"],
                weights=[0.33, 0.33, 0.33]
            )[0]

    def select_personality_traits(risk_tolerance):
        if risk_tolerance == "High Risk-Taker":
            return choices(["Extroverted", "Introverted"], weights=[0.8, 0.2])[0]
        elif risk_tolerance == "Moderate Risk-Taker":
            return choices(["Extroverted", "Introverted"], weights=[0.5, 0.5])[0]
        elif risk_tolerance == "Risk-Averse":
            return choices(["Extroverted", "Introverted"], weights=[0.3, 0.7])[0]
        else:
            return choices(["Extroverted", "Introverted"], weights=[0.5, 0.5])[0]

    def select_professional_network(age, job_title, education_level):

        if job_title in ["C-Suite", "Senior-Level"]:
            return "Extensive"
        elif education_level in ["Bachelor's degree", "Master's degree", "Doctorate degree"] and age in ["26-35",
                                                                                                         "36-45"]:
            return "Moderate"
        else:
            return "Basic"

    def select_decision_making_style(industry, age, motivation, pain_points):
        if industry in ["Software Development", "Finance", "Biotechnology"]:
            return "Data-Driven"
        elif "Time Management" in pain_points:
            return "Fast"
        elif age in ["45-60", "60+"] and motivation == "Stability":
            return "Cautious"
        elif motivation == "Innovation":
            return "Intuitive"
        elif "Complex Decision-Making Process" in pain_points:
            return "Peer-Influenced"
        else:
            return choices(["Fast", "Intuitive"], weights=[0.5, 0.5])[0]

    def select_motivations(personality_traits):
        if personality_traits == "Extroverted":
            return choices(
                ["Prestige", "Customer-Centricity", "Innovation", "Efficiency", "Stability"],
                weights=[0.4, 0.3, 0.2, 0.05, 0.05]
            )[0]
        elif personality_traits == "Introverted":
            return choices(
                ["Efficiency", "Stability", "Innovation", "Customer-Centricity", "Prestige"],
                weights=[0.4, 0.3, 0.2, 0.05, 0.05]
            )[0]
        else:
            return choices(
                ["Efficiency", "Innovation", "Customer-Centricity", "Prestige", "Stability"],
                weights=[0.2, 0.2, 0.2, 0.2, 0.2]
            )[0]

    def select_risk_tolerance(age, gender):
        if age in ["18-25", "26-35"]:
            return choices(
                ["Moderate Risk-Taker", "High Risk-Taker", "Risk-Averse"],
                weights=[0.5, 0.3, 0.2]
            )[0]
        elif gender == "Male":
            return choices(
                ["Moderate Risk-Taker", "Risk-Averse", "High Risk-Taker"],
                weights=[0.4, 0.4, 0.2]
            )[0]
        else:
            return "Risk-Averse"

    def select_decision_making_role(influence_structure):
        if influence_structure == "Highly centralized":
            return choices(MicroSegmentation.allowed_decision_making_role, weights=[0.6, 0.3, 0.1, 0.0])[0]
        elif influence_structure == "Moderately centralized":
            return choices(MicroSegmentation.allowed_decision_making_role, weights=[0.4, 0.4, 0.2, 0.0])[0]
        else:
            return choices(MicroSegmentation.allowed_decision_making_role, weights=[0.3, 0.5, 0.2, 0.0])[0]

    def select_technology_used(education_level, functional_field, work_environment):
        if education_level in ["Master's degree", "Doctorate degree"]:
            return choices(MicroSegmentation.allowed_tech_use, weights=[0.1, 0.4, 0.5, 0.0])[0]
        elif education_level in ["Bachelor's degree"]:
            return choices(MicroSegmentation.allowed_tech_use, weights=[0.2, 0.5, 0.3, 0.0])[0]
        elif functional_field in ["Technology & IT", "Product Management"]:
            return choices(MicroSegmentation.allowed_tech_use, weights=[0.1, 0.3, 0.6, 0.0])[0]
        elif work_environment == "Remote":
            return choices(MicroSegmentation.allowed_tech_use, weights=[0.2, 0.5, 0.3, 0.0])[0]
        else:
            return choices(MicroSegmentation.allowed_tech_use, weights=[0.4, 0.4, 0.2, 0.0])[0]

    def select_job_title_based_on_industry(industry, experience_level):
        if experience_level == "Entry-Level: 0-3 years":
            return "Entry-Level"
        elif experience_level == "Mid-Level: 4-10 years":
            return "Mid-Level"
        elif experience_level == "Senior-Level: 10+ years":
            return random.choice(["Senior-Level", "C-Suite"])  # General fallback for senior-level

    def select_work_environment(industry):
        if industry not in MicroSegmentation.allowed_industry_work_environment_weights:
            return "Industry not recognized."

        work_environments = MicroSegmentation.allowed_industry_work_environment_weights[industry]
        environments = list(work_environments.keys())
        weights = list(work_environments.values())

        selected_environment = random.choices(environments, weights=weights, k=1)[0]
        return selected_environment

    def select_functional_field(job_title):
        if job_title == "Entry-Level":
            fields = ["Finance & Accounting", "Operations", "Marketing & Communication", "Sales", "Technology & IT",
                      "Customer Service", "R&D", "Procurement", "Manufacturing", "Logistics"]
        elif job_title == "Mid-Level":
            fields = ["Finance & Accounting", "Operations", "Marketing & Communication", "Sales", "Technology & IT",
                      "Product Management", "Human Resources", "Legal & Compliance", "Customer Service", "R&D",
                      "Procurement", "Manufacturing", "Logistics"]
        elif job_title == "Senior-Level":
            fields = ["Finance & Accounting", "Operations", "Marketing & Communication", "Sales", "Technology & IT",
                      "Product Management", "Human Resources", "Legal & Compliance", "Customer Service", "R&D",
                      "Procurement", "Manufacturing", "Logistics"]
        elif job_title == "C-Suite":
            fields = ["Executive/Leadership", "Finance & Accounting", "Operations", "Marketing & Communication",
                      "Sales", "Technology & IT", "Product Management", "Human Resources", "Legal & Compliance", "R&D",
                      "Procurement", "Manufacturing", "Logistics"]
        else:
            return ["Finance & Accounting", "Operations", "Marketing & Communication", ]

        return random.choice(fields)

    def select_experience_level_based_on_age(age):
        if age == '18-25':
            return choices(MicroSegmentation.allowed_experience_level, weights=[0.8, 0.2, 0, 0])[0]
        elif age == '26-35':
            return choices(MicroSegmentation.allowed_experience_level, weights=[0.1, 0.6, 0.3, 0])[0]
        elif age == '36-45':
            return choices(MicroSegmentation.allowed_experience_level, weights=[0.05, 0.25, 0.7, 0])[0]
        else:
            return choices(MicroSegmentation.allowed_experience_level, weights=[0.05, 0.25, 0.7, 0])[0]

    def get_age(self):
        return self._age

    def set_age(self, value):
        if value not in self.allowed_age:
            raise ValueError(f"Age must be one of: {self.allowed_age}")
        self._age = value

    def get_gender(self):
        return self._gender

    def set_gender(self, value):
        if value not in self.allowed_gender:
            raise ValueError(f"Gender must be one of: {self.allowed_gender}")
        self._gender = value

    def get_location(self):
        return self._location

    def set_location(self, value):
        self._location = value

    def get_education_level(self):
        return self._education_level

    def set_education_level(self, value):
        if value not in self.allowed_education_level:
            raise ValueError(f"Education level must be one of: {self.allowed_education_level}")
        self._education_level = value

    def get_technology_used(self):
        return self._technology_used

    def set_technology_used(self, value):
        if value not in self.allowed_tech_use:
            raise ValueError(f"Technology use must be one of: {self.allowed_tech_use}")
        self._technology_used = value

    def get_job_title(self):
        return self._job_title

    def set_job_title(self, value):
        if value not in self.allowed_job_title:
            raise ValueError(f"Job title must be one of: {self.allowed_job_title}")
        self._job_title = value

    def get_experience_level(self):
        return self._experience_level

    def set_experience_level(self, value):
        if value not in self.allowed_experience_level:
            raise ValueError(f"Experience level must be one of: {self.allowed_experience_level}")
        self._experience_level = value

    def get_functional_field(self):
        return self._functional_field

    def set_functional_field(self, value):
        if value not in self.allowed_functional_field:
            raise ValueError(f"Functional field must be one of: {self.allowed_functional_field}")
        self._functional_field = value

    def get_decision_making_role(self):
        return self._decision_making_role

    def set_decision_making_role(self, value):
        if value not in self.allowed_decision_making_role:
            raise ValueError(f"Decision-making role must be one of: {self.allowed_decision_making_role}")
        self._decision_making_role = value

    def get_work_environment(self):
        return self._work_environment

    def set_work_environment(self, value):
        if value not in self.allowed_work_enviroment:
            raise ValueError(f"Work environment must be one of: {self.allowed_work_enviroment}")
        self._work_environment = value

    def get_professional_network(self):
        return self._professional_network

    def set_professional_network(self, value):
        self._professional_network = value

    def get_risk_tolerance(self):
        return self._risk_tolerance

    def set_risk_tolerance(self, value):
        if value not in self.allowed_risk_tolerance:
            raise ValueError(f"Risk tolerance must be one of: {self.allowed_risk_tolerance}")
        self._risk_tolerance = value

    def get_decision_making_style(self):
        return self._decision_making_style

    def set_decision_making_style(self, value):
        if value not in self.allowed_decision_making_style:
            raise ValueError(f"Decision-making style must be one of: {self.allowed_decision_making_style}")
        self._decision_making_style = value

    def get_motivations(self):
        return self._motivations

    def set_motivations(self, value):
        if value not in self.allowed_motivations:
            raise ValueError(f"Motivations must be one of: {self.allowed_motivations}")
        self._motivations = value

    def get_personality_traits(self):
        return self._personality_traits

    def set_personality_traits(self, value):
        if value not in self.allowed_personality_traits:
            raise ValueError(f"Personality traits must be one of: {self.allowed_personality_traits}")
        self._personality_traits = value

    def get_pain_points(self):
        return self._pain_points

    def set_pain_points(self, value):
        if value not in self.allowed_pain_points:
            raise ValueError(f"Pain points must be one of: {self.allowed_pain_points}")
        self._pain_points = value

    def get_kpis(self):
        return self._kpis

    def set_kpis(self, value):
        if value not in self.allowed_kpis['Business KPIs'] | \
                set(self.allowed_kpis['Marketing KPIs']) | \
                set(self.allowed_kpis['Product & Customer Service KPIs']) | \
                set(self.allowed_kpis['Human Resources KPIs']):
            raise ValueError(f"KPI must be one of: {self.allowed_kpis}")
        self._kpis = value

    def get_challenges(self):
        return self._challenges

    def set_challenges(self, value):
        if value not in self.allowed_challenges['General Business Challenges'] + \
                self.allowed_challenges['Marketing Challenges'] + \
                self.allowed_challenges['Sales Challenges'] + \
                self.allowed_challenges['Operation Challenges'] + \
                self.allowed_challenges['Product Challenges']:
            raise ValueError(f"Challenge must be one of: {self.allowed_challenges}")
        self._challenges = value

    def get_goals(self):
        return self._goals

    def set_goals(self, value):
        if value not in self.allowed_goals['General Business Goals'] + \
                self.allowed_goals['Sales Goals'] + \
                self.allowed_goals['Marketing Goals'] + \
                self.allowed_goals['Customer Service Goals'] + \
                self.allowed_goals['Operations Goals']:
            raise ValueError(f"Goal must be one of: {self.allowed_goals}")
        self._goals = value

    def __str__(self):
        return (
            f"ProfessionalProfile(\n"
            f"  Macro Segmentation: {self.macro_segmentation},\n"
            f"  Age: {self.age},\n"
            f"  Gender: {self.gender},\n"
            f"  Education Level: {self.education_level},\n"
            f"  Technology Used: {self.technology_used},\n"
            f"  Job Title: {self.job_title},\n"
            f"  Experience Level: {self.experience_level},\n"
            f"  Functional Field: {self.functional_field},\n"
            f"  Decision Making Role: {self.decision_making_role},\n"
            f"  Work Environment: {self.work_environment},\n"
            f"  Professional Network: {self.professional_network},\n"
            f"  Risk Tolerance: {self.risk_tolerance},\n"
            f"  Decision Making Style: {self.decision_making_style},\n"
            f"  Motivations: {self.motivations},\n"
            f"  Personality Traits: {self.personality_traits},\n"
            f"  Pain Points: {self.pain_points},\n"
            f"  KPIs: {self.kpis},\n"
            f"  Challenges: {self.challenges},\n"
            f"  Goals: {self.goals}\n"
            f")"
        )
