import random
from random import choices
from backend.database import db
from sqlalchemy.orm import relationship


class MacroSegmentation(db.Model):
    __tablename__ = 'macro_segmentation'
    id = db.Column(db.Integer, primary_key=True)
    input_fields_id = db.Column(db.Integer, db.ForeignKey('input_fields.id'), nullable=False)
    input_fields = relationship('InputFields', backref='macro_segments')  # Define relationship
    industry = db.Column(db.String(255), nullable=False)
    organization_size = db.Column(db.String(50), nullable=False)
    annual_revenue = db.Column(db.String(50), nullable=False)
    operational_regions = db.Column(db.Text, nullable=False)  # TO-DO why is this a text?
    market_density = db.Column(db.String(50), nullable=False)
    purchasing_frequency = db.Column(db.String(50), nullable=False)
    purchasing_volume = db.Column(db.String(50), nullable=False)
    technology_adoption = db.Column(db.String(50), nullable=False)
    usage_engagement_rate = db.Column(db.String(50), nullable=False)
    ownership_structure = db.Column(db.String(50), nullable=False)
    growth_stage = db.Column(db.String(50), nullable=False)
    influence_structure = db.Column(db.String(50), nullable=False)

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
                                  '5000+ employees', None]
    ALLOWED_REVENUE = ['Less than €1 million', '€1 million - €10 million', '€10 million - €50 million',
                       '€50 million - €100 million', None]

    ALLOWED_OPERATIONAL_REGIONS = ['Single country', 'Multi-country', 'Global presence', None]
    ALLOWED_MARKET_DENSITY = ['Urban', 'Suburban', 'Rural', None]

    ALLOWED_PURCH_FREQ = ['High-frequency buyers', 'Occasional buyers', 'Rare buyers', None]
    ALLOWED_PURCH_VOLUME = ['Small volume: < €50,000 per year', 'Medium volume: €50,000 - €500,000 per year',
                            'Large volume: > €500,000 per year', None]
    ALLOWED_TECH_ADOPTION = ['Early Adopters', 'Late Adopters', 'Technologically Conservative', None]
    ALLOWED_USAGE_RATE = ['Heavy users', 'Medium users', 'Light users', None]

    ALLOWED_OWNERSHIP_STRUCTURE = [
        'Private', 'Public', 'Non-Profit', 'Government-Owned or State-Owned Enterprises',
        'Franchise', 'Cooperatives', 'Partnerships', 'Sole Proprietorships', 'Venture-backed Start-ups', None
    ]
    ALLOWED_GROWTH_STAGE = ['Startup', 'Growth Stage', 'Maturity', 'Decline', 'Exit Stage', None]

    ALLOWED_INFLUENCE_STRUCT = [
        'Owner/Founder led', 'CEO/Executive Driven', 'Department-Driven',
        'Employee led', 'Board of Directors Involvement', None]

    industry_mappings = {
        "Agriculture, Forestry, Fishing and Hunting": [
            "Food and Beverage", "Environmental Services", "Biotechnology",
            "Chemicals", "Renewable Energy"
        ],
        "Mining, Quarrying, and Oil and Gas Extraction": [
            "Manufacturing", "Utilities", "Chemicals",
            "Logistics and Supply Chain", "Renewable Energy"
        ],
        "Utilities": [
            "Renewable Energy", "Construction", "Public Administration",
            "Environmental Services", "Telecommunications"
        ],
        "Construction": [
            "Real Estate Development", "Manufacturing", "Logistics and Supply Chain",
            "Utilities", "Environmental Services"
        ],
        "Manufacturing": [
            "Wholesale Trade", "Chemicals", "Automotive",
            "Aerospace and Defense", "Biotechnology"
        ],
        "Wholesale Trade": [
            "Retail Trade", "Logistics and Supply Chain", "Consumer Goods",
            "E-commerce", "Food and Beverage"
        ],
        "Retail Trade": [
            "Wholesale Trade", "E-commerce", "Consumer Goods",
            "Logistics and Supply Chain", "Textiles and Apparel"
        ],
        "Transportation and Warehousing": [
            "Logistics and Supply Chain", "Manufacturing", "Shipping and Maritime",
            "Automotive", "Aerospace and Defense"
        ],
        "Information": [
            "Software Development", "Media and Entertainment", "Telecommunications",
            "E-commerce", "Biotechnology"
        ],
        "Finance and Insurance": [
            "Real Estate", "Venture Capital and Private Equity", "Professional Services",
            "E-commerce", "Telecommunications"
        ],
        "Real Estate and Rental and Leasing": [
            "Construction", "Real Estate Development", "Finance and Insurance",
            "Tourism and Travel", "Hospitality"
        ],
        "Professional, Scientific, and Technical Services": [
            "Software Development", "Legal Services", "Biotechnology",
            "Telecommunications", "Environmental Services"
        ],
        "Management of Companies and Enterprises": [
            "Finance and Insurance", "Venture Capital and Private Equity",
            "Professional Services", "E-commerce", "Telecommunications"
        ],
        "Administrative and Support and Waste Management and Remediation Services": [
            "Environmental Services", "Construction", "Public Administration",
            "Utilities", "Waste Management"
        ],
        "Educational Services": [
            "Health Care and Social Assistance", "Software Development", "Nonprofit",
            "Tourism and Travel", "Telecommunications"
        ],
        "Health Care and Social Assistance": [
            "Pharmaceuticals", "Biotechnology", "Nonprofit",
            "Educational Services", "Government"
        ],
        "Arts, Entertainment, and Recreation": [
            "Media and Entertainment", "Tourism and Travel", "Hospitality",
            "Retail Trade", "Sports and Recreation"
        ],
        "Accommodation and Food Services": [
            "Tourism and Travel", "Hospitality", "Food and Beverage",
            "Retail Trade", "Real Estate Development"
        ],
        "Other Services (except Public Administration)": [
            "Retail Trade", "Nonprofit", "Hospitality",
            "Food and Beverage", "Telecommunications"
        ],
        "Public Administration": [
            "Utilities", "Health Care and Social Assistance", "Renewable Energy",
            "Education", "Legal Services"
        ],
        "Telecommunications": [
            "Software Development", "Information", "E-commerce",
            "Finance and Insurance", "Media and Entertainment"
        ],
        "Aerospace and Defense": [
            "Manufacturing", "Logistics and Supply Chain", "Software Development",
            "Automotive", "Biotechnology"
        ],
        "Biotechnology": [
            "Pharmaceuticals", "Health Care and Social Assistance", "Renewable Energy",
            "Software Development", "Environmental Services"
        ],
        "Chemicals": [
            "Manufacturing", "Agriculture, Forestry, Fishing and Hunting",
            "Renewable Energy", "Biotechnology", "Food and Beverage"
        ],
        "Consumer Goods": [
            "Retail Trade", "E-commerce", "Textiles and Apparel",
            "Manufacturing", "Wholesale Trade"
        ],
        "E-commerce": [
            "Retail Trade", "Wholesale Trade", "Software Development",
            "Finance and Insurance", "Logistics and Supply Chain"
        ],
        "Environmental Services": [
            "Waste Management", "Renewable Energy", "Construction",
            "Agriculture, Forestry, Fishing and Hunting", "Utilities"
        ],
        "Government": [
            "Public Administration", "Health Care and Social Assistance", "Utilities",
            "Legal Services", "Defense"
        ],
        "Legal Services": [
            "Government", "Finance and Insurance", "Real Estate Development",
            "Administrative Services", "Professional Services"
        ],
        "Media and Entertainment": [
            "Software Development", "E-commerce", "Telecommunications",
            "Retail Trade", "Tourism and Travel"
        ],
        "Pharmaceuticals": [
            "Biotechnology", "Health Care and Social Assistance", "Renewable Energy",
            "Chemicals", "Educational Services"
        ],
        "Renewable Energy": [
            "Utilities", "Environmental Services", "Construction",
            "Manufacturing", "Biotechnology"
        ],
        "Software Development": [
            "Information", "Telecommunications", "Finance and Insurance",
            "Biotechnology", "E-commerce"
        ],
        "Tourism and Travel": [
            "Hospitality", "Accommodation and Food Services", "Arts and Entertainment",
            "Transportation and Warehousing", "Retail Trade"
        ],
        "Automotive": [
            "Manufacturing", "Logistics and Supply Chain", "Transportation and Warehousing",
            "Retail Trade", "Chemicals"
        ],
        "Food and Beverage": [
            "Retail Trade", "Agriculture, Forestry, Fishing and Hunting",
            "Hospitality", "Manufacturing", "E-commerce"
        ],
        "Hospitality": [
            "Tourism and Travel", "Accommodation and Food Services", "Arts and Entertainment",
            "Retail Trade", "Real Estate Development"
        ],
        "Insurance": [
            "Finance and Insurance", "Health Care and Social Assistance", "Real Estate",
            "Automotive", "Professional Services"
        ],
        "Logistics and Supply Chain": [
            "Transportation and Warehousing", "Wholesale Trade", "Manufacturing",
            "Retail Trade", "E-commerce"
        ],
        "Nonprofit": [
            "Health Care and Social Assistance", "Educational Services", "Environmental Services",
            "Public Administration", "Arts and Entertainment"
        ],
        "Printing and Publishing": [
            "Media and Entertainment", "Retail Trade", "Software Development",
            "E-commerce", "Telecommunications"
        ],
        "Real Estate Development": [
            "Construction", "Finance and Insurance", "Hospitality",
            "Retail Trade", "Real Estate and Rental and Leasing"
        ],
        "Shipping and Maritime": [
            "Logistics and Supply Chain", "Transportation and Warehousing", "Retail Trade",
            "Wholesale Trade", "Aerospace and Defense"
        ],
        "Sports and Recreation": [
            "Arts and Entertainment", "Tourism and Travel", "Retail Trade",
            "Hospitality", "Media and Entertainment"
        ],
        "Textiles and Apparel": [
            "Manufacturing", "Retail Trade", "E-commerce",
            "Consumer Goods", "Wholesale Trade"
        ],
        "Venture Capital and Private Equity": [
            "Finance and Insurance", "Software Development", "Biotechnology",
            "E-commerce", "Professional Services"
        ],
        "Waste Management": [
            "Environmental Services", "Construction", "Utilities",
            "Public Administration", "Manufacturing"
        ],
        "Wood Products": [
            "Construction", "Manufacturing", "Environmental Services",
            "Agriculture, Forestry, Fishing and Hunting", "Wholesale Trade"
        ],
        "Zoological and Botanical Gardens": [
            "Tourism and Travel", "Environmental Services", "Educational Services",
            "Nonprofit", "Arts and Entertainment"
        ]
    }

    def __init__(self, input_fields, industry, organization_size, annual_revenue, operational_regions,
                 market_density, purchasing_frequency, purchasing_volume, technology_adoption,
                 usage_engagement_rate, ownership_structure, growth_stage, influence_structure):
        if operational_regions not in self.ALLOWED_OPERATIONAL_REGIONS:
            raise ValueError(f"Operational regions must be one of: {self.ALLOWED_OPERATIONAL_REGIONS}")
        if market_density not in self.ALLOWED_MARKET_DENSITY:
            raise ValueError(f"Market density must be one of: {self.ALLOWED_MARKET_DENSITY}")
        if purchasing_frequency not in self.ALLOWED_PURCH_FREQ:
            raise ValueError(f"Purchasing frequency must be one of: {self.ALLOWED_PURCH_FREQ}")
        if purchasing_volume not in self.ALLOWED_PURCH_VOLUME:
            raise ValueError(f"Purchasing volume must be one of: {self.ALLOWED_PURCH_VOLUME}")
        if technology_adoption not in self.ALLOWED_TECH_ADOPTION:
            raise ValueError(f"Technology adoption must be one of: {self.ALLOWED_TECH_ADOPTION}")
        if usage_engagement_rate not in self.ALLOWED_USAGE_RATE:
            raise ValueError(f"Usage engagement rate must be one of: {self.ALLOWED_USAGE_RATE}")
        if ownership_structure not in self.ALLOWED_OWNERSHIP_STRUCTURE:
            raise ValueError(f"Ownership structure must be one of: {self.ALLOWED_OWNERSHIP_STRUCTURE}")
        if growth_stage not in self.ALLOWED_GROWTH_STAGE:
            raise ValueError(f"Growth stage must be one of: {self.ALLOWED_GROWTH_STAGE}")
        if influence_structure not in self.ALLOWED_INFLUENCE_STRUCT:
            raise ValueError(f"Influence structure must be one of: {self.ALLOWED_INFLUENCE_STRUCT}")

        self.input_fields = input_fields
        self.industry = industry
        self.organization_size = organization_size
        self.annual_revenue = annual_revenue
        self.operational_regions = operational_regions
        self.market_density = market_density
        self.purchasing_frequency = purchasing_frequency
        self.purchasing_volume = purchasing_volume
        self.technology_adoption = technology_adoption
        self.usage_engagement_rate = usage_engagement_rate
        self.ownership_structure = ownership_structure
        self.growth_stage = growth_stage
        self.influence_structure = influence_structure

    def select_org_size_based_on_industry(industry):
        size_distribution = {
            "Agriculture, Forestry, Fishing and Hunting": [0.6, 0.3, 0.1, 0.0, 0.0],
            "Mining, Quarrying, and Oil and Gas Extraction": [0.2, 0.2, 0.3, 0.2, 0.1],
            "Utilities": [0.1, 0.2, 0.3, 0.3, 0.1],
            "Manufacturing": [0.05, 0.15, 0.3, 0.3, 0.2],
            "Retail Trade": [0.4, 0.3, 0.2, 0.05, 0.05],
            "Software Development": [0.3, 0.3, 0.2, 0.1, 0.1],
            "Pharmaceuticals": [0.1, 0.2, 0.3, 0.2, 0.2],
            "Renewable Energy": [0.1, 0.2, 0.3, 0.3, 0.1],
            "Nonprofit": [0.8, 0.15, 0.05, 0.0, 0.0],
            "Zoological and Botanical Gardens": [0.85, 0.1, 0.05, 0.0, 0.0],
            "Aerospace and Defense": [0.05, 0.1, 0.2, 0.3, 0.35],
            "Telecommunications": [0.05, 0.1, 0.2, 0.3, 0.35],
            "Finance and Insurance": [0.1, 0.2, 0.3, 0.2, 0.2],
            "Media and Entertainment": [0.4, 0.3, 0.2, 0.05, 0.05],
        }
        default_distribution = [0.2, 0.3, 0.3, 0.1, 0.1]
        weights = size_distribution.get(industry, default_distribution)
        return choices(MacroSegmentation.ALLOWED_ORGANIZATION_SIZES[:-1], weights=weights)[0]  # Exclude 'None'

    def select_revenue_based_on_size(org_size):
        if org_size == '1-10 employees':
            return choices(MacroSegmentation.ALLOWED_REVENUE, weights=[0.8, 0.15, 0.05, 0, 0])[0]
        elif org_size == '11-50 employees':
            return choices(MacroSegmentation.ALLOWED_REVENUE, weights=[0.6, 0.3, 0.1, 0, 0])[0]
        elif org_size == '51-500 employees':
            return choices(MacroSegmentation.ALLOWED_REVENUE, weights=[0.2, 0.5, 0.3, 0, 0])[0]
        else:  # '501-5000 employees'
            return choices(MacroSegmentation.ALLOWED_REVENUE, weights=[0.1, 0.3, 0.4, 0.2, 0])[0]

    def select_purchasing_volume_based_on_size(org_size):
        if org_size == '1-10 employees':
            return 'Small volume: < €50,000 per year'
        elif org_size == '11-50 employees':
            return choices(['Small volume: < €50,000 per year', 'Medium volume: €50,000 - €500,000 per year'],
                           weights=[0.5, 0.5])[0]
        elif org_size == '51-500 employees':
            return 'Medium volume: €50,000 - €500,000 per year'
        else:  # '501+ employees'
            return 'Large volume: > €500,000 per year'

    def select_technology_adoption_based_on_industry(industry):
        high_tech_industries = ['Biotechnology', 'Pharmaceuticals', 'Renewable Energy']
        if industry in high_tech_industries:
            return choices(MacroSegmentation.ALLOWED_TECH_ADOPTION, weights=[0.7, 0.2, 0.1, 0])[0]
        else:
            return choices(MacroSegmentation.ALLOWED_TECH_ADOPTION, weights=[0.2, 0.5, 0.3, 0])[0]

    def select_ownership_structure_based_on_industry(industry):
        if industry in ['Agriculture, Forestry, Fishing and Hunting', 'Mining, Quarrying, and Oil and Gas Extraction']:

            return choices(
                MacroSegmentation.ALLOWED_OWNERSHIP_STRUCTURE,
                weights=[0.4, 0.1, 0.05, 0.3, 0.05, 0.05, 0.05, 0, 0, 0]
            )[0]
        elif industry in ['Biotechnology', 'Pharmaceuticals', 'Software Development']:

            return choices(
                MacroSegmentation.ALLOWED_OWNERSHIP_STRUCTURE,
                weights=[0.2, 0.3, 0.05, 0.05, 0.1, 0.05, 0.05, 0.05, 0.15, 0]
            )[0]
        elif industry in ['Retail Trade', 'Accommodation and Food Services']:

            return choices(
                MacroSegmentation.ALLOWED_OWNERSHIP_STRUCTURE,
                weights=[0.3, 0.2, 0.05, 0.05, 0.2, 0.05, 0.1, 0.05, 0, 0]
            )[0]
        elif industry in ['Nonprofit', 'Educational Services', 'Health Care and Social Assistance']:

            return choices(
                MacroSegmentation.ALLOWED_OWNERSHIP_STRUCTURE,
                weights=[0.1, 0.1, 0.5, 0.2, 0, 0.05, 0, 0, 0, 0]
            )[0]
        elif industry in ['Construction', 'Manufacturing', 'Transportation and Warehousing']:

            return choices(
                MacroSegmentation.ALLOWED_OWNERSHIP_STRUCTURE,
                weights=[0.5, 0.2, 0.05, 0.05, 0, 0.05, 0.1, 0.05, 0, 0]
            )[0]
        elif industry in ['Finance and Insurance', 'Professional, Scientific, and Technical Services']:

            return choices(
                MacroSegmentation.ALLOWED_OWNERSHIP_STRUCTURE,
                weights=[0.3, 0.4, 0.05, 0.05, 0, 0.1, 0.05, 0, 0.05, 0]
            )[0]
        else:

            return choices(
                MacroSegmentation.ALLOWED_OWNERSHIP_STRUCTURE,
                weights=[0.4, 0.3, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0, 0]
            )[0]

    def select_market_density(industry, org_size):
        urban_industries = [
            "Software Development", "Finance and Insurance", "Media and Entertainment",
            "Professional, Scientific, and Technical Services"
        ]
        rural_industries = [
            "Agriculture, Forestry, Fishing and Hunting", "Mining, Quarrying, and Oil and Gas Extraction"
        ]

        if industry in urban_industries:
            return choices(MacroSegmentation.ALLOWED_MARKET_DENSITY[:-1], weights=[0.7, 0.2, 0.1])[0]
        elif industry in rural_industries:
            return choices(MacroSegmentation.ALLOWED_MARKET_DENSITY[:-1], weights=[0.1, 0.3, 0.6])[0]
        else:
            if org_size in ['1-10 employees', '11-50 employees']:
                return choices(MacroSegmentation.ALLOWED_MARKET_DENSITY[:-1], weights=[0.4, 0.4, 0.2])[0]
            elif org_size in ['51-500 employees']:
                return choices(MacroSegmentation.ALLOWED_MARKET_DENSITY[:-1], weights=[0.5, 0.3, 0.2])[0]
            else:
                return choices(MacroSegmentation.ALLOWED_MARKET_DENSITY[:-1], weights=[0.6, 0.3, 0.1])[0]

    def select_usage_engagement_rate(industry):
        high_engagement_industries = [
            "E-commerce", "Media and Entertainment", "Software Development"
        ]
        low_engagement_industries = [
            "Mining, Quarrying, and Oil and Gas Extraction", "Utilities"
        ]

        if industry in high_engagement_industries:
            return choices(MacroSegmentation.ALLOWED_USAGE_RATE[:-1], weights=[0.6, 0.3, 0.1])[0]
        elif industry in low_engagement_industries:
            return choices(MacroSegmentation.ALLOWED_USAGE_RATE[:-1], weights=[0.2, 0.4, 0.4])[0]
        else:
            return choices(MacroSegmentation.ALLOWED_USAGE_RATE[:-1], weights=[0.4, 0.4, 0.2])[0]

    def select_growth_stage_based_on_size(org_size):
        if org_size == '1-10 employees':
            return choices(['Startup', 'Exit Stage'], weights=[0.8, 0.2])[0]
        elif org_size == '11-50 employees':
            return choices(['Startup', 'Growth Stage'], weights=[0.4, 0.6])[0]
        elif org_size == '51-500 employees':
            return choices(['Growth Stage', 'Maturity'], weights=[0.5, 0.5])[0]
        elif org_size == '501-5000 employees':
            return choices(['Growth Stage', 'Maturity', 'Decline'], weights=[0.3, 0.5, 0.2])[0]
        else:  # '5000+ employees'
            return choices(['Maturity', 'Decline', 'Exit Stage'], weights=[0.5, 0.3, 0.2])[0]

    def select_influence_structure(industry, growth_stage):
        founder_led_industries = ["Software Development", "Biotechnology", "Pharmaceuticals"]
        board_dominated_growth_stages = ["Maturity", "Decline", "Exit Stage"]

        if industry in founder_led_industries and growth_stage == "Startup":
            return "Owner/Founder led"
        elif growth_stage in board_dominated_growth_stages:
            return "Board of Directors Involvement"
        elif growth_stage == "Growth Stage":
            return "CEO/Executive Driven"
        else:
            return random.choice(MacroSegmentation.ALLOWED_INFLUENCE_STRUCT[:-1])

    def select_purchasing_frecuency(industry):
        if industry in ['Biotechnology', 'Pharmaceuticals', 'Renewable Energy']:
            return choices(MacroSegmentation.ALLOWED_PURCH_FREQ, weights=[0.5, 0.4, 0.1, 0])[0]
        else:
            return choices(MacroSegmentation.ALLOWED_PURCH_FREQ, weights=[0.2, 0.5, 0.3, 0])[0]

    def select_related_industry(input_industry):

        related_industries = MacroSegmentation.industry_mappings.get(input_industry,
                                                                     MacroSegmentation.ALLOWED_INDUSTRIES)

        selected_industry = random.choice(related_industries)

        return selected_industry

    def generate_macro(input_fields):
        industry = MacroSegmentation.select_related_industry(input_fields.get_industry)
        organization_size = MacroSegmentation.select_org_size_based_on_industry(industry)
        revenue = MacroSegmentation.select_revenue_based_on_size(organization_size)
        operational_region = choices(MacroSegmentation.ALLOWED_OPERATIONAL_REGIONS, weights=[0.6, 0.3, 0.1, 0])[0]
        market_density = MacroSegmentation.select_market_density(industry, organization_size)
        purchasing_frequency = MacroSegmentation.select_purchasing_frecuency(industry)

        purchasing_volume = MacroSegmentation.select_purchasing_volume_based_on_size(organization_size)
        technology_adoption = MacroSegmentation.select_technology_adoption_based_on_industry(industry)
        usage_engagement_rate = MacroSegmentation.select_usage_engagement_rate(industry)
        ownership_structure = MacroSegmentation.select_ownership_structure_based_on_industry(industry)
        growth_stage = MacroSegmentation.select_growth_stage_based_on_size(organization_size)
        influence_structure = MacroSegmentation.select_influence_structure(industry, growth_stage)

        return MacroSegmentation(
            input_fields=input_fields,
            industry=industry,
            organization_size=organization_size,
            annual_revenue=revenue,
            operational_regions=str(operational_region),
            market_density=market_density,
            purchasing_frequency=purchasing_frequency,
            purchasing_volume=purchasing_volume,
            technology_adoption=technology_adoption,
            usage_engagement_rate=usage_engagement_rate,
            ownership_structure=ownership_structure,
            growth_stage=growth_stage,
            influence_structure=influence_structure
        )

    def get_inputFields(self):
        return self.inputFields

    def set_inputFields(self, inputFields):
        self.inputFields = inputFields

    def get_industry(self):
        return self.industry

    def set_industry(self, industry):
        if industry not in self.allowed_industries:
            raise ValueError(f"Industry must be one of: {self.allowed_industries}")
        self.industry = industry

    def get_organization_size(self):
        return self.organization_size

    def set_organization_size(self, organization_size):
        if organization_size not in self.allowed_org_size:
            raise ValueError(f"Organization size must be one of: {self.allowed_org_size}")
        self.organization_size = organization_size

    def get_annual_revenue(self):
        return self.annual_revenue

    def set_annual_revenue(self, annual_revenue):
        if annual_revenue not in self.allowed_revenue:
            raise ValueError(f"Annual revenue must be one of: {self.allowed_revenue}")
        self.annual_revenue = annual_revenue

    def get_operational_regions(self):
        return self.operational_regions

    def set_operational_regions(self, operational_regions):
        if operational_regions not in self.allowed_operational_regions:
            raise ValueError(f"Operational regions must be one of: {self.allowed_operational_regions}")
        self.operational_regions = operational_regions

    def get_market_density(self):
        return self.market_density

    def set_market_density(self, market_density):
        if market_density not in self.allowed_market_density:
            raise ValueError(f"Market density must be one of: {self.allowed_market_density}")
        self.market_density = market_density

    def get_purchasing_frequency(self):
        return self.purchasing_frequency

    def set_purchasing_frequency(self, purchasing_frequency):
        if purchasing_frequency not in self.allowed_purchasing_frequency:
            raise ValueError(f"Purchasing frequency must be one of: {self.allowed_purchasing_frequency}")
        self.purchasing_frequency = purchasing_frequency

    def get_purchasing_volume(self):
        return self.purchasing_volume

    def set_purchasing_volume(self, purchasing_volume):
        if purchasing_volume not in self.allowed_purchasing_volume:
            raise ValueError(f"Purchasing volume must be one of: {self.allowed_purchasing_volume}")
        self.purchasing_volume = purchasing_volume

    def get_technology_adoption(self):
        return self.technology_adoption

    def set_technology_adoption(self, technology_adoption):
        if technology_adoption not in self.allowed_technology_adoption:
            raise ValueError(f"Technology adoption must be one of: {self.allowed_technology_adoption}")
        self.technology_adoption = technology_adoption

    def get_usage_engagement_rate(self):
        return self.usage_engagement_rate

    def set_usage_engagement_rate(self, usage_engagement_rate):
        if usage_engagement_rate not in self.allowed_usage_engagement_rate:
            raise ValueError(f"Usage engagement rate must be one of: {self.allowed_usage_engagement_rate}")
        self.usage_engagement_rate = usage_engagement_rate

    def get_ownership_structure(self):
        return self.ownership_structure

    def set_ownership_structure(self, ownership_structure):
        if ownership_structure not in self.allowed_ownership_structure:
            raise ValueError(f"Ownership structure must be one of: {self.allowed_ownership_structure}")
        self.ownership_structure = ownership_structure

    def get_growth_stage(self):
        return self.growth_stage

    def set_growth_stage(self, growth_stage):
        if growth_stage not in self.allowed_growth_stage:
            raise ValueError(f"Growth stage must be one of: {self.allowed_growth_stage}")
        self.growth_stage = growth_stage

    def get_influence_structure(self):
        return self.influence_structure

    def set_influence_structure(self, influence_structure):
        if influence_structure not in self.allowed_influence_structure:
            raise ValueError(f"Influence structure must be one of: {self.allowed_influence_structure}")
        self.influence_structure = influence_structure

    def __str__(self):
        """Custom string representation of the object."""
        return (
            f"Macro Object Details:\n"
            f"Industry: {self.industry}\n"
            f"Organization Size: {self.organization_size}\n"
            f"Annual Revenue: {self.annual_revenue}\n"
            f"Operational Regions: {self.operational_regions}\n"
            f"Market Density: {self.market_density}\n"
            f"Purchasing Frequency: {self.purchasing_frequency}\n"
            f"Purchasing Volume: {self.purchasing_volume}\n"
            f"Technology Adoption: {self.technology_adoption}\n"
            f"Usage Engagement Rate: {self.usage_engagement_rate}\n"
            f"Ownership Structure: {self.ownership_structure}\n"
            f"Growth Stage: {self.growth_stage}\n"
            f"Influence Structure: {self.influence_structure}\n"
        )
