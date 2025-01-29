import random
from random import choices
from backend.database import db
from sqlalchemy.dialects.mysql import JSON


class InputFields(db.Model):
    __tablename__ = 'input_fields'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    industry = db.Column(db.String(255), nullable=False)
    organization_size = db.Column(db.String(50), nullable=False)
    annual_revenue = db.Column(db.String(50), nullable=False)
    location = db.Column(JSON, nullable=False)  # JSON-encoded list of locations #TO-DO this should be a String
    geographical_focus = db.Column(db.String(50), nullable=False)
    strategic_positioning = db.Column(JSON, nullable=False)  # JSON-encoded list of strategic positions
    competitors = db.Column(JSON, nullable=False, default=[])  # JSON-encoded list of locations #this should be a text

    # Allowed Inputs
    ALLOWED_INDUSTRIES = [
        "Agriculture, Forestry, Fishing and Hunting",
        "Mining, Quarrying, and Oil and Gas Extraction",
        "Utilities",
        "Construction",
        "Manufacturing",
        "Wholesale Trade",
        "Retail Trade",
        "Transportation and Warehousing",
        "Information",
        "Finance and Insurance",
        "Real Estate and Rental and Leasing",
        "Professional, Scientific, and Technical Services",
        "Management of Companies and Enterprises",
        "Administrative and Support and Waste Management and Remediation Services",
        "Educational Services",
        "Health Care and Social Assistance",
        "Arts, Entertainment, and Recreation",
        "Accommodation and Food Services",
        "Other Services (except Public Administration)",
        "Public Administration",
        "Telecommunications",
        "Aerospace and Defense",
        "Biotechnology",
        "Chemicals",
        "Consumer Goods",
        "E-commerce",
        "Environmental Services",
        "Government",
        "Legal Services",
        "Media and Entertainment",
        "Pharmaceuticals",
        "Renewable Energy",
        "Software Development",
        "Tourism and Travel",
        "Automotive",
        "Food and Beverage",
        "Hospitality",
        "Insurance",
        "Logistics and Supply Chain",
        "Nonprofit",
        "Printing and Publishing",
        "Real Estate Development",
        "Retail and Consumer Goods",
        "Shipping and Maritime",
        "Sports and Recreation",
        "Textiles and Apparel",
        "Venture Capital and Private Equity",
        "Waste Management",
        "Wood Products",
        "Zoological and Botanical Gardens"
    ]
    ALLOWED_ORGANIZATION_SIZES = ['1-10 employees', '11-50 employees', '51-500 employees', '501-5000 employees',
                                  '5000+ employees']
    ALLOWED_REVENUE = ['Less than €1 million', '€1 million - €10 million', '€10 million - €50 million',
                       '€50 million - €100 million']
    ALLOWED_GEO_FOCUS = ['A specific country', 'Multiple countries', 'A region', 'Global']
    ALLOWED_STRATEGIC_POSITIONING = ['Cost Leader', 'Differentiator', 'Customer-Centricity', 'Niche Focus',
                                     "Innovation Leader", 'Sustainability Focus', 'Quality Leader',
                                     'Market Penetration']

    ALLOWED_LOCATIONS = [
        # Africa
        "Northern Africa",
        "West Africa",
        "East Africa",
        "Central Africa",
        "Southern Africa",

        # Americas
        "North America",
        "Central America",
        "Caribbean",
        "South America",

        # Asia
        "East Asia",
        "Southeast Asia",
        "South Asia",
        "Central Asia",
        "Western Asia",

        # Europe
        "Western Europe",
        "Northern Europe",
        "Southern Europe",
        "Eastern Europe",

        # Oceania
        "Australia and New Zealand",
        "Melanesia",
        "Micronesia",
        "Polynesia",
    ]

    location_weights = [
        # Africa
        0.05, 0.05, 0.05, 0.05, 0.05,
        # Americas
        0.3, 0.2, 0.1, 0.2,
        # Asia
        0.05, 0.05, 0.05, 0.05, 0.05,
        # Europe
        0.3, 0.3, 0.3, 0.3,
        # Oceania
        0.05, 0.01, 0.01, 0.01,
    ]

    def __init__(self, industry, organization_size, annual_revenue, location, geographical_focus,
                 strategic_positioning):
        if industry not in self.ALLOWED_INDUSTRIES:
            raise ValueError(f"Industry must be one of: {self.ALLOWED_INDUSTRIES}")
        if organization_size not in self.ALLOWED_ORGANIZATION_SIZES:
            raise ValueError(f"Organization size must be one of: {self.ALLOWED_ORGANIZATION_SIZES}")
        if annual_revenue not in self.ALLOWED_REVENUE:
            raise ValueError(f"Annual revenue must be one of: {self.ALLOWED_REVENUE}")
        if geographical_focus not in self.ALLOWED_GEO_FOCUS:
            raise ValueError(f"Geographical focus must be one of: {self.ALLOWED_GEO_FOCUS}")
        if not all(pos in self.ALLOWED_STRATEGIC_POSITIONING for pos in strategic_positioning):
            raise ValueError(f"Each strategic positioning must be one of: {self.ALLOWED_STRATEGIC_POSITIONING}")
        if not all(loc in self.ALLOWED_LOCATIONS for loc in location):
            raise ValueError(f"Each location must be one of: {self.ALLOWED_LOCATIONS}")

        self.industry = industry
        self.organization_size = organization_size
        self.annual_revenue = annual_revenue
        self.location = location
        self.geographical_focus = geographical_focus
        self.strategic_positioning = strategic_positioning

    @staticmethod
    def select_revenue_based_on_size(org_size):
        if org_size == '1-10 employees':
            return choices(InputFields.ALLOWED_REVENUE, weights=[0.8, 0.15, 0.05, 0])[0]
        elif org_size == '11-50 employees':
            return choices(InputFields.ALLOWED_REVENUE, weights=[0.6, 0.3, 0.1, 0])[0]
        elif org_size == '51-500 employees':
            return choices(InputFields.ALLOWED_REVENUE, weights=[0.2, 0.5, 0.3, 0])[0]
        elif org_size == '501-5000 employees':
            return choices(InputFields.ALLOWED_REVENUE, weights=[0.1, 0.3, 0.4, 0.2])[0]
        else:
            return choices(InputFields.ALLOWED_REVENUE, weights=[0.1, 0.2, 0.5, 0.3])[0]

    @staticmethod
    def select_geographical_focus(org_size, industry):
        high_value_industries = {
            "Software Development", "Pharmaceuticals", "Biotechnology",
            "Aerospace and Defense", "Renewable Energy", "Telecommunications"
        }
        non_physical_industries = {
            "Software Development", "Information", "Media and Entertainment",
            "E-commerce", "Finance and Insurance", "Professional, Scientific, and Technical Services"
        }

        # Determine if the industry matches high-value or non-physical categories
        high_value_product = industry in high_value_industries
        non_physical_product = industry in non_physical_industries

        # Base weights for geographical focus by organization size
        if org_size == '1-10 employees':
            focus_weights = [0.7, 0.2, 0.1, 0.0]  # [specific country, multiple countries, region, global]
        elif org_size == '11-50 employees':
            focus_weights = [0.5, 0.3, 0.2, 0.0]
        elif org_size == '51-500 employees':
            focus_weights = [0.3, 0.4, 0.2, 0.1]
        else:  # '501-5000 employees'
            focus_weights = [0.1, 0.3, 0.3, 0.3]  # Larger companies more likely to have global focus

        # Adjust weights based on industry characteristics
        if high_value_product:
            # High-value industries are more likely to have broader or global reach
            focus_weights = [focus_weights[0] * 0.5, focus_weights[1] * 1.2, focus_weights[2] * 1.5,
                             focus_weights[3] * 2]
        if non_physical_product:
            # Non-physical products likely to scale globally
            focus_weights = [focus_weights[0] * 0.7, focus_weights[1] * 1.1, focus_weights[2] * 1.2,
                             focus_weights[3] * 1.5]

        # Normalize weights
        total_weight = sum(focus_weights)
        focus_weights = [w / total_weight for w in focus_weights]

        return choices(InputFields.ALLOWED_GEO_FOCUS, weights=focus_weights)[0]

    @staticmethod
    def select_strategic_positioning(industry):
        positioning_options = {
            "Agriculture, Forestry, Fishing and Hunting": ["Cost Leader", "Sustainability Focus"],
            "Mining, Quarrying, and Oil and Gas Extraction": ["Cost Leader", "Sustainability Focus", "Quality Leader"],
            "Utilities": ["Quality Leader", "Sustainability Focus"],
            "Manufacturing": ["Cost Leader", "Quality Leader", "Innovation Leader"],
            "Retail Trade": ["Customer-Centricity", "Cost Leader", "Differentiator"],
            "Software Development": ["Innovation Leader", "Customer-Centricity", "Niche Focus"],
            "Pharmaceuticals": ["Innovation Leader", "Quality Leader"],
            "Renewable Energy": ["Sustainability Focus", "Innovation Leader"],
            "Nonprofit": ["Sustainability Focus", "Customer-Centricity"],
            "Zoological and Botanical Gardens": ["Sustainability Focus", "Niche Focus"],
        }
        options = positioning_options.get(industry, InputFields.ALLOWED_STRATEGIC_POSITIONING)
        return random.sample(options, k=random.randint(1, min(len(options), 3)))

    @staticmethod
    def select_org_size_based_on_industry(industry):
        size_distribution = {
            "Agriculture, Forestry, Fishing and Hunting": [0.6, 0.25, 0.1, 0.05, 0.0],
            "Mining, Quarrying, and Oil and Gas Extraction": [0.2, 0.2, 0.3, 0.2, 0.1],
            "Utilities": [0.1, 0.2, 0.3, 0.3, 0.1],
            "Manufacturing": [0.05, 0.15, 0.3, 0.3, 0.2],
            "Retail Trade": [0.3, 0.3, 0.2, 0.1, 0.1],
            "Software Development": [0.2, 0.3, 0.3, 0.1, 0.1],
            "Pharmaceuticals": [0.05, 0.15, 0.3, 0.3, 0.2],
            "Renewable Energy": [0.05, 0.2, 0.3, 0.3, 0.15],
            "Nonprofit": [0.7, 0.2, 0.05, 0.05, 0.0],
            "Zoological and Botanical Gardens": [0.85, 0.1, 0.05, 0.0, 0.0],
            "Aerospace and Defense": [0.05, 0.1, 0.2, 0.3, 0.35],
            "Telecommunications": [0.05, 0.1, 0.2, 0.3, 0.35],
            "Finance and Insurance": [0.1, 0.2, 0.3, 0.2, 0.2],
            "Media and Entertainment": [0.3, 0.3, 0.2, 0.1, 0.1],
        }
        default_distribution = [0.2, 0.3, 0.3, 0.1, 0.1]  # Default for unspecified industries
        weights = size_distribution.get(industry, default_distribution)
        return choices(InputFields.ALLOWED_ORGANIZATION_SIZES, weights=weights)[0]

    @staticmethod
    def select_strategic_positioning_based_on_industry(industry):
        positioning_options = {
            "Agriculture, Forestry, Fishing and Hunting": ["Cost Leader", "Sustainability Focus"],
            "Mining, Quarrying, and Oil and Gas Extraction": ["Cost Leader", "Sustainability Focus", "Quality Leader"],
            "Utilities": ["Quality Leader", "Sustainability Focus"],
            "Manufacturing": ["Cost Leader", "Quality Leader", "Innovation Leader"],
            "Retail Trade": ["Customer-Centricity", "Cost Leader", "Differentiator"],
            "Software Development": ["Innovation Leader", "Customer-Centricity", "Niche Focus"],
            "Pharmaceuticals": ["Innovation Leader", "Quality Leader"],
            "Renewable Energy": ["Sustainability Focus", "Innovation Leader"],
            "Nonprofit": ["Sustainability Focus", "Customer-Centricity"],
            "Zoological and Botanical Gardens": ["Sustainability Focus", "Niche Focus"],
        }
        options = positioning_options.get(industry, InputFields.ALLOWED_STRATEGIC_POSITIONING)
        return random.sample(options, k=random.randint(1, min(len(options), 3)))

    @staticmethod
    def generate_inputs():
        industry = random.choice(InputFields.ALLOWED_INDUSTRIES)
        org_size = InputFields.select_org_size_based_on_industry(industry)
        revenue = InputFields.select_revenue_based_on_size(org_size)
        geographical_focus = InputFields.select_geographical_focus(org_size,
                                                                   industry)  ##if bigger compnay more board (if non phycial product or high-value products it doesnt matter)
        strategic_positioning = InputFields.select_strategic_positioning_based_on_industry(industry)
        locations = choices(population=InputFields.ALLOWED_LOCATIONS, weights=InputFields.location_weights,
                            k=random.randint(1, 3)
                            )

        return InputFields(
            industry=industry,
            organization_size=org_size,
            annual_revenue=revenue,
            location=locations,
            geographical_focus=geographical_focus,
            strategic_positioning=strategic_positioning
        )

    def get_competitors(self):
        return self.competitors

    def set_competitors(self, id):
        self.competitors = id

    def get_name(self):
        return self.name

    def set_name(self, id):
        self.name = id

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_industry(self):
        return self.industry

    def set_industry(self, industry):
        if industry not in self.ALLOWED_INDUSTRIES:
            raise ValueError(f"Industry must be one of: {self.ALLOWED_INDUSTRIES}")
        self.industry = industry

    def get_organization_size(self):
        return self.organization_size

    def set_organization_size(self, organization_size):
        if organization_size not in self.ALLOWED_ORGANIZATION_SIZES:
            raise ValueError(f"Organization size must be one of: {self.ALLOWED_ORGANIZATION_SIZES}")
        self.organization_size = organization_size

    def get_annual_revenue(self):
        return self.annual_revenue

    def set_annual_revenue(self, annual_revenue):
        if annual_revenue not in self.ALLOWED_REVENUE:
            raise ValueError(f"Annual revenue must be one of: {self.ALLOWED_REVENUE}")
        self.annual_revenue = annual_revenue

    def get_location(self):
        return self.location

    def set_location(self, location):
        if not all(loc in self.ALLOWED_LOCATIONS for loc in location):
            raise ValueError(f"Each location must be one of: {self.ALLOWED_LOCATIONS}")
        self.location = location

    def get_geographical_focus(self):
        return self.geographical_focus

    def set_geographical_focus(self, geographical_focus):
        if geographical_focus not in self.ALLOWED_GEO_FOCUS:
            raise ValueError(f"Geographical focus must be one of: {self.ALLOWED_GEO_FOCUS}")
        self.geographical_focus = geographical_focus

    def get_strategic_positioning(self):
        return self.strategic_positioning

    def set_strategic_positioning(self, strategic_positioning):
        if not all(pos in self.ALLOWED_STRATEGIC_POSITIONING for pos in strategic_positioning):
            raise ValueError(f"Each strategic positioning must be one of: {self.ALLOWED_STRATEGIC_POSITIONING}")
        self.strategic_positioning = strategic_positioning
