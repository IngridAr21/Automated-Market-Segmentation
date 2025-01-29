from random import choices
from backend.database import db
from sqlalchemy.orm import relationship


class CustomerJourney(db.Model):
    __tablename__ = 'customer_journey'
    id = db.Column(db.Integer, primary_key=True)
    micro_segmentation_id = db.Column(db.Integer, db.ForeignKey('micro_segmentation.id'), nullable=False)
    micro_segmentation = relationship('MicroSegmentation', backref='customer_journeys')  # Define relationship

    awareness = db.Column(db.String(255), nullable=False)
    consideration = db.Column(db.String(255), nullable=False)
    decision_making = db.Column(db.String(255), nullable=False)
    purchase = db.Column(db.String(255), nullable=False)
    service = db.Column(db.String(255), nullable=False)
    loyalty = db.Column(db.String(255), nullable=False)
    ambassador = db.Column(db.String(255), nullable=False)

    # Awareness Stage
    allowed_awareness = ['Trade Shows/Conferences', 'Networking Events', 'Business Cards/Merchandise',
                         'Word of Mouth', 'Social Media Ads', 'Webinars/Online Conferences',
                         'Digital PR / Content Marketing', 'Influencer Marketing',
                         'Programmatic Advertising', 'Influencer Webinars/Interviews',
                         'Video Ads', 'Podcast Appearances/Advertisements', None]

    # Consideration Stage
    allowed_consideration = ['Onsite Product Demos', 'Workshops/Seminars', 'Printed Case Studies/Testimonials',
                             'Industry Awards/Recognition', 'Office/Facility Tours', 'Website',
                             'Online Demos/Virtual Consultations', 'Customer Reviews/Testimonials',
                             'Comparison Tools', 'Retargeting Ads', 'Interactive Product Configurators',
                             'Interactive FAQ or AI Chatbots', None]

    # Decision-Making Stage
    allowed_decisionMaking = ['Face-to-Face Negotiations', 'In-Person Product Trials / Meetings',
                              'Third-Party Meetings', 'Proposal via Email/Online Portal',
                              'Online Product Demos', 'ROI Calculators', None]

    # Purchase Stage
    allowed_purchase = ['Face-to-Face Contract Signing', 'Product/Service Handover Meeting',
                        'Onsite Delivery or Setup', 'E-commerce/Ordering Portals',
                        'E-invoicing', 'Dynamic Pricing Tools', 'Custom Payment Portals',
                        'Purchase Confirmation Emails', None]

    # Service Stage
    allowed_service = ['Maintenance Visits', 'Dedicated Account Manager', 'Help Desk/Support Portal',
                       'Online Training/Webinars', 'Video Tutorials', 'Live Chat/Chatbots for Support', None]

    # Loyalty Stage
    allowed_loyalty = ['Loyalty Programs (Physical Rewards)', 'Customer Appreciation Events',
                       'Physical Awards/Recognition', 'Branded Gifting Programs',
                       'Subscription Services (Digital Renewal)', 'Automated Personalization',
                       'Automated Renewal Reminders', 'Exclusive Access to Content',
                       'Loyalty Emails/Discount Offers', 'Gamified Loyalty Programs', None]

    # Ambassador Stage
    allowed_ambassador = ['Referral Program (Physical Rewards)', 'Customer Advisory Board (In-Person Meetings)',
                          'Invitations to Product Launches or Corporate Events', 'Referral Program (Digital Rewards)',
                          'Social Media Sharing', 'Affiliate or Influencer Partnerships', None]

    def __init__(self, micro_segmentation, awareness, consideration, decision_making, purchase, service, loyalty,
                 ambassador):

        if awareness not in self.allowed_awareness:
            raise ValueError(f"Awareness stage touchpoint must be one of: {self.allowed_awareness}")

        if consideration not in self.allowed_consideration:
            raise ValueError(f"Consideration stage touchpoint must be one of: {self.allowed_consideration}")

        if decision_making not in self.allowed_decisionMaking:
            raise ValueError(f"Decision Making stage touchpoint must be one of: {self.allowed_decisionMaking}")

        if purchase not in self.allowed_purchase:
            raise ValueError(f"Purchase stage touchpoint must be one of: {self.allowed_purchase}  ")

        if service not in self.allowed_service:
            raise ValueError(f"Service stage touchpoint must be one of: {self.allowed_service}")

        if loyalty not in self.allowed_loyalty:
            raise ValueError(f"Loyalty stage touchpoint must be one of: {self.allowed_loyalty}")

        if ambassador not in self.allowed_ambassador:
            raise ValueError(f"Ambassador stage touchpoint must be one of: {self.allowed_ambassador}")

        self.micro_segmentation = micro_segmentation
        self.awareness = awareness
        self.consideration = consideration
        self.decision_making = decision_making
        self.purchase = purchase
        self.service = service
        self.loyalty = loyalty
        self.ambassador = ambassador

    def generate_customer_journey(micro):
        """
        Generate a customer's journey based on micro-segmentation and stage-specific conditions,
        incorporating influence weights.
        """
        if micro.macro_segmentation is None:
            raise ValueError("MicroSegmentation is not linked to a MacroSegmentation instance")

        # Awareness Stage
        awareness_touchpoints, awareness_weights = CustomerJourney.select_awareness_stage(
            industry=micro.macro_segmentation.get_industry(),
            revenue=micro.macro_segmentation.get_annual_revenue(),
            market_density=micro.macro_segmentation.get_market_density(),
            tech_use=micro.technology_used,
            tech_adoption=micro.macro_segmentation.get_technology_adoption(),
            decision_style=micro.decision_making_style
        )

        # Consideration Stage
        consideration_touchpoints, consideration_weights = CustomerJourney.select_consideration_stage(
            industry=micro.macro_segmentation.get_industry(),
            tech_use=micro.technology_used,
            work_environment=micro.work_environment,
            age=micro.age,
            tech_adoption=micro.macro_segmentation.get_technology_adoption(),
            decision_style=micro.decision_making_style
        )

        # Decision-Making Stage
        decision_making_touchpoints, decision_making_weights = CustomerJourney.select_decision_making_stage(
            work_environment=micro.work_environment,
            tech_use=micro.technology_used,
            market_density=micro.macro_segmentation.get_market_density(),
            tech_adoption=micro.macro_segmentation.get_technology_adoption(),
            decision_style=micro.decision_making_style
        )

        # Purchase Stage
        purchase_touchpoints, purchase_weights = CustomerJourney.select_purchase_stage(
            industry=micro.macro_segmentation.get_industry(),
            revenue=micro.macro_segmentation.get_annual_revenue(),
            market_density=micro.macro_segmentation.get_market_density(),
            tech_use=micro.technology_used,
            tech_adoption=micro.macro_segmentation.get_technology_adoption(),
            decision_style=micro.decision_making_style
        )

        # Service Stage
        service_touchpoints, service_weights = CustomerJourney.select_service_stage(
            industry=micro.macro_segmentation.get_industry(),
            tech_use=micro.technology_used,
            market_density=micro.macro_segmentation.get_market_density(),
            work_environment=micro.work_environment,
            tech_adoption=micro.macro_segmentation.get_technology_adoption(),
            decision_style=micro.decision_making_style
        )

        # Validación de puntos seleccionados
        for touchpoint in service_touchpoints:
            if touchpoint not in CustomerJourney.allowed_service:
                raise ValueError(
                    f"Service stage touchpoint '{touchpoint}' is invalid. Must be one of: {CustomerJourney.allowed_service}")

        # Loyalty Stage
        loyalty_touchpoints, loyalty_weights = CustomerJourney.select_loyalty_stage(
            industry=micro.macro_segmentation.get_industry(),
            revenue=micro.macro_segmentation.get_annual_revenue(),
            tech_use=micro.technology_used,
            market_density=micro.macro_segmentation.get_market_density(),
            age=micro.age,
            work_environment=micro.work_environment,
            tech_adoption=micro.macro_segmentation.get_technology_adoption(),
            decision_style=micro.decision_making_style
        )

        # Ambassador Stage
        ambassador_touchpoints, ambassador_weights = CustomerJourney.select_ambassador_stage(
            industry=micro.macro_segmentation.get_industry(),
            revenue=micro.macro_segmentation.get_annual_revenue(),
            market_density=micro.macro_segmentation.get_market_density(),
            age=micro.age,
            tech_use=micro.technology_used,
            tech_adoption=micro.macro_segmentation.get_technology_adoption(),
            decision_style=micro.decision_making_style
        )

        return CustomerJourney(
            micro_segmentation=micro,
            awareness=awareness_touchpoints[0],
            consideration=consideration_touchpoints[0],
            decision_making=decision_making_touchpoints[0],
            purchase=purchase_touchpoints[0],
            service=service_touchpoints[0],
            loyalty=loyalty_touchpoints[0],
            ambassador=ambassador_touchpoints[0]
        )

    @staticmethod
    def normalize_weights(weights):
        weights = [float(w) for w in weights if isinstance(w, (int, float)) or w.isdigit()]

        total = sum(weights)
        if total == 0:
            raise ValueError("The total of weights is zero; cannot normalize.")
        return [w / total for w in weights]

    def select_awareness_stage(industry, revenue, market_density, tech_use, tech_adoption, decision_style):
        """
        Select touchpoints for the Awareness Stage based on industry, revenue, market_density, tech_use,
        tech_adoption, and decision-making style.
        """
        touchpoints = [
            'Trade Shows/Conferences', 'Networking Events', 'Business Cards/Merchandise',
            'Word of Mouth', 'Social Media Ads', 'Webinars/Online Conferences',
            'Digital PR / Content Marketing', 'Influencer Marketing',
            'Programmatic Advertising', 'Influencer Webinars/Interviews',
            'Video Ads', 'Podcast Appearances/Advertisements'
        ]

        if industry in ['Retail',
                        'Hospitality'] and revenue == 'Less than €1 million' and market_density == 'Urban' and tech_use == 'High':
            weights = [0.0476, 0.0238, 0.0238, 0.0476, 0.1667, 0.1190, 0.1190, 0.1429, 0.1429, 0.0952, 0.1190, 0.0714]
        elif tech_adoption == 'Early Adopters' and decision_style == 'Collaborative':
            weights = [0.1273, 0.1091, 0.0909, 0.0909, 0.1273, 0.1455, 0.1273, 0.1455, 0.1455, 0.1273, 0.1091, 0.0727]
        elif industry in ['Technology',
                          'IT Services'] and revenue == '€1 million - €10 million' and tech_use == 'Medium':
            weights = [0.1, 0.1, 0.1, 0.05, 0.2, 0.15, 0.15, 0.1, 0.1, 0.05, 0.1, 0.05]
        elif market_density == 'Suburban' and decision_style == 'Hierarchical':
            weights = [0.1, 0.08, 0.08, 0.1, 0.12, 0.12, 0.12, 0.1, 0.1, 0.1, 0.08, 0.08]
        elif industry == 'Healthcare' and tech_adoption == 'Late Majority':
            weights = [0.08, 0.06, 0.06, 0.08, 0.14, 0.14, 0.14, 0.12, 0.12, 0.1, 0.08, 0.08]
        elif revenue == '€10 million - €50 million' and market_density == 'Rural' and tech_use == 'Low':
            weights = [0.05, 0.05, 0.05, 0.1, 0.15, 0.1, 0.1, 0.2, 0.2, 0.05, 0.05, 0.05]
        elif industry in ['E-commerce', 'Media'] and tech_use == 'High' and decision_style == 'Data-Driven':
            weights = [0.05, 0.05, 0.05, 0.1, 0.2, 0.15, 0.15, 0.1, 0.1, 0.05, 0.05, 0.05]
        else:
            weights = [1 / len(touchpoints)] * len(touchpoints)

        selected_touchpoints = choices(touchpoints, weights=weights, k=3)
        return selected_touchpoints, weights

    def select_consideration_stage(industry, tech_use, work_environment, age, tech_adoption, decision_style):

        touchpoints = [
            'Onsite Product Demos', 'Workshops/Seminars', 'Printed Case Studies/Testimonials',
            'Industry Awards/Recognition', 'Office/Facility Tours', 'Website',
            'Online Demos/Virtual Consultations', 'Customer Reviews/Testimonials',
            'Comparison Tools', 'Retargeting Ads', 'Interactive Product Configurators',
            'Interactive FAQ or AI Chatbots'
        ]

        if industry == 'Software Development' and tech_use == 'High' and work_environment == 'Remote' and age == '18-35':
            weights = [0.1034, 0.0747, 0.0598, 0.0598, 0.0598, 0.1195, 0.1345, 0.1195, 0.1046, 0.1345, 0.1345, 0.1195]
        elif tech_adoption == 'Early Adopters' and decision_style == 'Hierarchical':
            weights = [0.0857, 0.0571, 0.0571, 0.0571, 0.0714, 0.1000, 0.1143, 0.1000, 0.0857, 0.1143, 0.1143, 0.1000]
        elif industry in ['Healthcare',
                          'Pharmaceuticals'] and tech_use == 'Medium' and work_environment == 'Office-Based':
            weights = [0.1, 0.1, 0.08, 0.08, 0.08, 0.12, 0.12, 0.1, 0.1, 0.08, 0.08, 0.06]
        elif work_environment == 'Hybrid' and decision_style == 'Collaborative' and tech_adoption == 'Majority':
            weights = [0.1, 0.08, 0.08, 0.08, 0.1, 0.12, 0.12, 0.1, 0.1, 0.1, 0.08, 0.08]
        elif industry in ['Retail', 'E-commerce'] and age == '26-45' and tech_use == 'High':
            weights = [0.08, 0.08, 0.06, 0.06, 0.06, 0.14, 0.14, 0.12, 0.1, 0.1, 0.1, 0.06]
        elif tech_adoption == 'Late Adopters' and decision_style == 'Data-Driven':
            weights = [0.07, 0.07, 0.05, 0.05, 0.05, 0.13, 0.13, 0.13, 0.1, 0.1, 0.1, 0.07]
        elif work_environment == 'Field-Based' and tech_use == 'Low':
            weights = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05, 0.05]
        elif industry in ['Finance', 'Banking'] and tech_adoption == 'Innovators' and decision_style == 'Intuitive':
            weights = [0.08, 0.08, 0.06, 0.06, 0.06, 0.15, 0.15, 0.12, 0.1, 0.1, 0.08, 0.08]
        else:
            weights = [1 / len(touchpoints)] * len(touchpoints)

        selected_touchpoints = choices(touchpoints, weights=weights, k=3)
        return selected_touchpoints, weights

    def select_decision_making_stage(work_environment, tech_use, market_density, tech_adoption, decision_style):

        if work_environment == 'Office-Based' and tech_use == 'High' and market_density == 'Urban':
            weights = [0.1860, 0.1628, 0.1163, 0.2093, 0.2093, 0.1860]
        elif tech_adoption == 'Late Adopters' and decision_style == 'Collaborative':
            weights = [0.1429, 0.1190, 0.1429, 0.1905, 0.1905, 0.1667]
        elif market_density == 'Suburban' and work_environment == 'Hybrid' and decision_style == 'Hierarchical':
            weights = [0.15, 0.15, 0.12, 0.2, 0.2, 0.18]
        elif work_environment == 'Remote' and tech_use == 'Medium' and decision_style == 'Data-Driven':
            weights = [0.14, 0.13, 0.15, 0.18, 0.2, 0.2]
        elif tech_adoption == 'Innovators' and decision_style == 'Intuitive' and market_density == 'Urban':
            weights = [0.2, 0.15, 0.1, 0.2, 0.2, 0.15]
        elif work_environment == 'Field-Based' and tech_use == 'Low' and market_density == 'Rural':
            weights = [0.18, 0.18, 0.14, 0.18, 0.16, 0.16]
        elif tech_adoption == 'Majority' and decision_style == 'Consensus-Based' and market_density == 'Suburban':
            weights = [0.16, 0.14, 0.12, 0.2, 0.2, 0.18]
        else:
            weights = [0.1163, 0.0930, 0.1395, 0.1628, 0.1860, 0.2093]

        touchpoints = [
            'Face-to-Face Negotiations', 'In-Person Product Trials / Meetings',
            'Third-Party Meetings', 'Proposal via Email/Online Portal',
            'Online Product Demos', 'ROI Calculators'
        ]
        selected_touchpoints = choices(touchpoints, weights=weights, k=2)
        return selected_touchpoints, weights

    def select_purchase_stage(industry, revenue, market_density, tech_use, tech_adoption, decision_style):

        if revenue == '€50 million - €100 million' and market_density == 'Urban' and tech_use == 'High':
            weights = [0.1538, 0.1368, 0.1197, 0.1026, 0.1538, 0.1538, 0.1538, 0.1368]
        elif tech_adoption == 'Majority' and decision_style == 'Collaborative':
            weights = [0.1429, 0.1250, 0.1071, 0.0893, 0.1429, 0.1429, 0.1429, 0.1250]
        elif industry in ['E-commerce', 'Retail'] and tech_use == 'Medium' and market_density == 'Urban':
            weights = [0.12, 0.1, 0.09, 0.2, 0.15, 0.15, 0.12, 0.07]
        elif industry == 'Manufacturing' and revenue == '€10 million - €50 million' and market_density == 'Suburban':
            weights = [0.14, 0.13, 0.11, 0.09, 0.14, 0.14, 0.14, 0.11]
        elif tech_adoption == 'Early Adopters' and decision_style == 'Data-Driven':
            weights = [0.13, 0.12, 0.1, 0.1, 0.15, 0.15, 0.15, 0.1]
        elif industry == 'Finance' and tech_use == 'Low' and market_density == 'Rural':
            weights = [0.16, 0.14, 0.13, 0.1, 0.13, 0.13, 0.13, 0.08]
        elif tech_adoption == 'Late Majority' and decision_style == 'Hierarchical' and revenue == 'Less than €1 million':
            weights = [0.15, 0.13, 0.11, 0.08, 0.13, 0.13, 0.13, 0.11]
        else:  # Default for undefined scenarios
            weights = [0.1111, 0.0926, 0.0741, 0.0741, 0.1296, 0.1296, 0.1296, 0.1111]

        touchpoints = [
            'Face-to-Face Contract Signing', 'Product/Service Handover Meeting',
            'Onsite Delivery or Setup', 'E-commerce/Ordering Portals',
            'E-invoicing', 'Dynamic Pricing Tools', 'Custom Payment Portals',
            'Purchase Confirmation Emails'
        ]
        selected_touchpoints = choices(touchpoints, weights=weights, k=2)
        return selected_touchpoints, weights

    def select_service_stage(industry, tech_use, market_density, work_environment, tech_adoption, decision_style):

        if industry == 'Finance' and tech_use == 'High' and market_density == 'Urban' and work_environment == 'Remote':
            weights = [0.1250, 0.1667, 0.1458, 0.1875, 0.1667, 0.1875]
        elif tech_adoption == 'Late Adopters' and decision_style == 'Hierarchical':
            weights = [0.1250, 0.1875, 0.1563, 0.1875, 0.1875, 0.1563]
        elif industry == 'Healthcare' and work_environment == 'On-Site' and tech_use == 'Medium':
            weights = [0.2, 0.15, 0.2, 0.15, 0.15, 0.15]
        elif tech_adoption == 'Early Adopters' and decision_style == 'Data-Driven' and work_environment == 'Remote':
            weights = [0.1, 0.1, 0.2, 0.2, 0.2, 0.2]
        elif market_density == 'Rural' and tech_use == 'Low' and industry in ['Agriculture', 'Construction']:
            weights = [0.25, 0.2, 0.15, 0.15, 0.15, 0.1]
        elif industry == 'Technology' and tech_use == 'High' and work_environment == 'Hybrid':
            weights = [0.1, 0.15, 0.15, 0.2, 0.2, 0.2]
        elif market_density == 'Suburban' and tech_adoption == 'Majority' and decision_style == 'Collaborative':
            weights = [0.15, 0.15, 0.2, 0.2, 0.15, 0.15]
        else:
            weights = [0.1429, 0.2000, 0.1714, 0.1714, 0.1714, 0.1429]

        touchpoints = [
            'Maintenance Visits', 'Dedicated Account Manager', 'Help Desk/Support Portal',
            'Online Training/Webinars', 'Video Tutorials', 'Live Chat/Chatbots for Support'
        ]
        selected_touchpoints = choices(touchpoints, weights=weights, k=2)
        return selected_touchpoints, weights

    def select_loyalty_stage(industry, revenue, tech_use, market_density, age, work_environment, tech_adoption,
                             decision_style):

        if revenue == '€50 million - €100 million' and tech_use == 'High' and age == '18-35' and work_environment == 'Remote':
            weights = [0.0889, 0.0778, 0.0667, 0.0889, 0.1, 0.0889, 0.1, 0.1, 0.1, 0.1]
        elif tech_adoption == 'Majority' and decision_style == 'Collaborative':
            weights = [0.0854, 0.0732, 0.0610, 0.0854, 0.0976, 0.0854, 0.0976, 0.0976, 0.0976, 0.0976]
        elif industry == 'Retail' and age in ['36-45', '46-55'] and decision_style == 'Customer-Centric':
            weights = [0.1, 0.1, 0.1, 0.1, 0.15, 0.1, 0.1, 0.15, 0.1, 0.1]
        elif work_environment == 'Hybrid' and tech_adoption == 'Early Adopters' and tech_use == 'Medium':
            weights = [0.07, 0.08, 0.07, 0.08, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
        elif market_density == 'Suburban' and decision_style == 'Data-Driven' and revenue == '€10 million - €50 million':
            weights = [0.1, 0.08, 0.08, 0.08, 0.12, 0.1, 0.1, 0.1, 0.12, 0.1]
        elif industry == 'Technology' and tech_use == 'High' and age == '18-25' and decision_style == 'Fast':
            weights = [0.05, 0.05, 0.05, 0.1, 0.15, 0.1, 0.15, 0.15, 0.1, 0.1]
        else:
            weights = [0.0714, 0.0714, 0.0571, 0.0857, 0.0857, 0.0714, 0.1, 0.0857, 0.1, 0.0857]

        touchpoints = [
            'Loyalty Programs (Physical Rewards)', 'Customer Appreciation Events',
            'Physical Awards/Recognition', 'Branded Gifting Programs',
            'Subscription Services (Digital Renewal)', 'Automated Personalization',
            'Automated Renewal Reminders', 'Exclusive Access to Content',
            'Loyalty Emails/Discount Offers', 'Gamified Loyalty Programs'
        ]
        selected_touchpoints = choices(touchpoints, weights=weights, k=2)
        return selected_touchpoints, weights

    def select_ambassador_stage(industry, revenue, market_density, age, tech_use, tech_adoption, decision_style):

        if industry in ['Retail Trade', 'E-commerce',
                        'Media and Entertainment'] and tech_use == 'High' and age == '18-35' and market_density == 'Urban':
            weights = [0.1667, 0.1481, 0.1667, 0.1667, 0.1667, 0.1667]
        elif tech_adoption == 'Late Majority' and decision_style == 'Hierarchical':
            weights = [0.1667, 0.1458, 0.1667, 0.1667, 0.1667, 0.1667]
        elif revenue in ['€10 million - €50 million',
                         '€50 million - €100 million'] and market_density == 'Suburban' and tech_use == 'Medium':
            weights = [0.15, 0.15, 0.1, 0.15, 0.2, 0.25]
        elif age in ['36-45', '46-55'] and decision_style == 'Collaborative' and industry == 'Technology':
            weights = [0.1, 0.2, 0.15, 0.15, 0.2, 0.2]
        elif industry == 'Finance' and tech_use == 'Low' and market_density == 'Rural' and tech_adoption == 'Early Adopters':
            weights = [0.2, 0.2, 0.15, 0.1, 0.15, 0.2]
        elif market_density == 'Urban' and decision_style == 'Customer-Centric' and age == '26-35':
            weights = [0.2, 0.15, 0.2, 0.15, 0.15, 0.15]
        else:  # Default case for suburban/rural density or low tech use
            weights = [0.1667, 0.1429, 0.1667, 0.1667, 0.1667, 0.1667]

        touchpoints = [
            'Referral Program (Physical Rewards)', 'Customer Advisory Board (In-Person Meetings)',
            'Invitations to Product Launches or Corporate Events', 'Referral Program (Digital Rewards)',
            'Social Media Sharing', 'Affiliate or Influencer Partnerships'
        ]
        selected_touchpoints = choices(touchpoints, weights=weights, k=2)
        return selected_touchpoints, weights

    @staticmethod
    def pad_weights(weights, max_length):
        """
        Pads the weights vector with zeros until it reaches the specified max_length.
        If the vector is longer than max_length, raise an error.
        """

        if 12 > max_length:
            raise ValueError("Weights vector exceeds the maximum length")

        return weights + [0] * (max_length - len(weights))

    def select_stage_with_influence(stage_touchpoints, conditional_weights, influence_map):

        if isinstance(conditional_weights, list):
            weights = conditional_weights
        elif isinstance(conditional_weights, tuple) and len(conditional_weights) == 2:
            _, weights = conditional_weights
        else:
            raise ValueError("conditional_weights should be a list or a tuple (touchpoints, weights)")



        try:
            # Ensure all weights are numeric
            weights = [float(w) for w in weights if isinstance(w, (int, float)) or str(w).replace('.', '', 1).isdigit()]
        except ValueError as e:

            raise ValueError(f"Invalid weights provided: {weights}. Ensure all weights are numeric.") from e



        weights = CustomerJourney.pad_weights(weights, len(stage_touchpoints))


        normalized_weights = CustomerJourney.normalize_weights(weights)


        combined_weights = [
            normalized_weights[i] * (
                sum(influence_map.get(stage_touchpoints[i], {}).values()) / len(
                    influence_map.get(stage_touchpoints[i], {}))
                if stage_touchpoints[i] in influence_map and isinstance(influence_map.get(stage_touchpoints[i]),
                                                                        dict) else 1
            )
            for i in range(len(stage_touchpoints))
        ]


        normalized_combined_weights = CustomerJourney.normalize_weights(combined_weights)

        return choices(stage_touchpoints, weights=normalized_combined_weights, k=3)

    def __str__(self):
        return (
            f"CustomerJourney("
            f"Micro Segmentation: {self.micro_segmentation}, "
            f"Awareness: {self.awareness}, "
            f"Consideration: {self.consideration}, "
            f"Decision Making: {self.decision_making}, "
            f"Purchase: {self.purchase}, "
            f"Service: {self.service}, "
            f"Loyalty: {self.loyalty}, "
            f"Ambassador: {self.ambassador})"
        )

    influence_maps = {
        "awareness_to_consideration": {
            "Trade Shows/Conferences": {
                "Onsite Product Demos": 0.1111,
                "Workshops/Seminars": 0.0972,
                "Printed Case Studies/Testimonials": 0.0833,
                "Industry Awards/Recognition": 0.0694,
                "Office/Facility Tours": 0.0972,
                "Website": 0.0833,
                "Online Demos/Virtual Consultations": 0.0694,
                "Customer Reviews/Testimonials": 0.0972,
                "Comparison Tools": 0.0833,
                "Retargeting Ads": 0.0694,
                "Interactive Product Configurators": 0.0694,
                "Interactive FAQ or AI Chatbots": 0.0694,
            },
            "Networking Events": {
                "Onsite Product Demos": 0.0875,
                "Workshops/Seminars": 0.0750,
                "Printed Case Studies/Testimonials": 0.0875,
                "Industry Awards/Recognition": 0.1000,
                "Office/Facility Tours": 0.0750,
                "Website": 0.0625,
                "Online Demos/Virtual Consultations": 0.0750,
                "Customer Reviews/Testimonials": 0.1000,
                "Comparison Tools": 0.0625,
                "Retargeting Ads": 0.0750,
                "Interactive Product Configurators": 0.0875,
                "Interactive FAQ or AI Chatbots": 0.0750,
            },
            "Business Cards/Merchandise": {
                "Onsite Product Demos": 0.0909,
                "Workshops/Seminars": 0.1091,
                "Printed Case Studies/Testimonials": 0.0909,
                "Industry Awards/Recognition": 0.1091,
                "Office/Facility Tours": 0.0909,
                "Website": 0.1273,
                "Online Demos/Virtual Consultations": 0.1091,
                "Customer Reviews/Testimonials": 0.0909,
                "Comparison Tools": 0.0909,
                "Retargeting Ads": 0.1091,
                "Interactive Product Configurators": 0.1091,
                "Interactive FAQ or AI Chatbots": 0.0909,
            },
            "Word of Mouth": {
                "Onsite Product Demos": 0.0714,
                "Workshops/Seminars": 0.0714,
                "Printed Case Studies/Testimonials": 0.0952,
                "Industry Awards/Recognition": 0.0833,
                "Office/Facility Tours": 0.0714,
                "Website": 0.0714,
                "Online Demos/Virtual Consultations": 0.0595,
                "Customer Reviews/Testimonials": 0.1071,
                "Comparison Tools": 0.0714,
                "Retargeting Ads": 0.0595,
                "Interactive Product Configurators": 0.0595,
                "Interactive FAQ or AI Chatbots": 0.0714,
            },
            "Social Media Ads": {
                "Onsite Product Demos": 0.0667,
                "Workshops/Seminars": 0.0667,
                "Printed Case Studies/Testimonials": 0.0556,
                "Industry Awards/Recognition": 0.0667,
                "Office/Facility Tours": 0.0556,
                "Website": 0.0889,
                "Online Demos/Virtual Consultations": 0.1000,
                "Customer Reviews/Testimonials": 0.0778,
                "Comparison Tools": 0.0889,
                "Retargeting Ads": 0.1000,
                "Interactive Product Configurators": 0.0778,
                "Interactive FAQ or AI Chatbots": 0.0889,
            },
            "Webinars/Online Conferences": {
                "Onsite Product Demos": 0.0833,
                "Workshops/Seminars": 0.1111,
                "Printed Case Studies/Testimonials": 0.0972,
                "Industry Awards/Recognition": 0.0694,
                "Office/Facility Tours": 0.0694,
                "Website": 0.0833,
                "Online Demos/Virtual Consultations": 0.1111,
                "Customer Reviews/Testimonials": 0.0833,
                "Comparison Tools": 0.0694,
                "Retargeting Ads": 0.0694,
                "Interactive Product Configurators": 0.0833,
                "Interactive FAQ or AI Chatbots": 0.1111,
            },
            "Digital PR / Content Marketing": {
                "Onsite Product Demos": 0.0833,
                "Workshops/Seminars": 0.0694,
                "Printed Case Studies/Testimonials": 0.1111,
                "Industry Awards/Recognition": 0.1250,
                "Office/Facility Tours": 0.0972,
                "Website": 0.0972,
                "Online Demos/Virtual Consultations": 0.0833,
                "Customer Reviews/Testimonials": 0.1111,
                "Comparison Tools": 0.0972,
                "Retargeting Ads": 0.0694,
                "Interactive Product Configurators": 0.0694,
                "Interactive FAQ or AI Chatbots": 0.0833,
            },
            "Influencer Marketing": {
                "Onsite Product Demos": 0.0625,
                "Workshops/Seminars": 0.0625,
                "Printed Case Studies/Testimonials": 0.0625,
                "Industry Awards/Recognition": 0.0875,
                "Office/Facility Tours": 0.0625,
                "Website": 0.1000,
                "Online Demos/Virtual Consultations": 0.1000,
                "Customer Reviews/Testimonials": 0.1125,
                "Comparison Tools": 0.0750,
                "Retargeting Ads": 0.0625,
                "Interactive Product Configurators": 0.0625,
                "Interactive FAQ or AI Chatbots": 0.0875,
            },
            "Programmatic Advertising": {
                "Onsite Product Demos": 0.0667,
                "Workshops/Seminars": 0.0800,
                "Printed Case Studies/Testimonials": 0.0667,
                "Industry Awards/Recognition": 0.0800,
                "Office/Facility Tours": 0.0667,
                "Website": 0.1200,
                "Online Demos/Virtual Consultations": 0.1067,
                "Customer Reviews/Testimonials": 0.0933,
                "Comparison Tools": 0.1067,
                "Retargeting Ads": 0.1200,
                "Interactive Product Configurators": 0.0933,
                "Interactive FAQ or AI Chatbots": 0.0933,
            },
            "Influencer Webinars/Interviews": {
                "Onsite Product Demos": 0.0870,
                "Workshops/Seminars": 0.1000,
                "Printed Case Studies/Testimonials": 0.0750,
                "Industry Awards/Recognition": 0.0625,
                "Office/Facility Tours": 0.0625,
                "Website": 0.0750,
                "Online Demos/Virtual Consultations": 0.0870,
                "Customer Reviews/Testimonials": 0.1000,
                "Comparison Tools": 0.0870,
                "Retargeting Ads": 0.0625,
                "Interactive Product Configurators": 0.0750,
                "Interactive FAQ or AI Chatbots": 0.1000,
            },
            "Video Ads": {
                "Onsite Product Demos": 0.0833,
                "Workshops/Seminars": 0.0694,
                "Printed Case Studies/Testimonials": 0.0694,
                "Industry Awards/Recognition": 0.0833,
                "Office/Facility Tours": 0.0694,
                "Website": 0.1250,
                "Online Demos/Virtual Consultations": 0.1111,
                "Customer Reviews/Testimonials": 0.0833,
                "Comparison Tools": 0.1111,
                "Retargeting Ads": 0.1111,
                "Interactive Product Configurators": 0.0833,
                "Interactive FAQ or AI Chatbots": 0.0972,
            },
            "Podcast Appearances/Advertisements": {
                "Onsite Product Demos": 0.0714,
                "Workshops/Seminars": 0.0714,
                "Printed Case Studies/Testimonials": 0.1000,
                "Industry Awards/Recognition": 0.1143,
                "Office/Facility Tours": 0.0857,
                "Website": 0.0857,
                "Online Demos/Virtual Consultations": 0.0857,
                "Customer Reviews/Testimonials": 0.1143,
                "Comparison Tools": 0.0714,
                "Retargeting Ads": 0.0857,
                "Interactive Product Configurators": 0.0714,
                "Interactive FAQ or AI Chatbots": 0.0714,
            },
        },
        "consideration_to_decision_making": {
            "Onsite Product Demos": {
                "Face-to-Face Negotiations": 0.186,
                "In-Person Product Trials / Meetings": 0.163,
                "Third-Party Meetings": 0.140,
                "Proposal via Email/Online Portal": 0.140,
                "Online Product Demos": 0.209,
                "ROI Calculators": 0.163,
            },
            "Workshops/Seminars": {
                "Face-to-Face Negotiations": 0.184,
                "In-Person Product Trials / Meetings": 0.211,
                "Third-Party Meetings": 0.132,
                "Proposal via Email/Online Portal": 0.158,
                "Online Product Demos": 0.158,
                "ROI Calculators": 0.158,
            },
            "Printed Case Studies/Testimonials": {
                "Face-to-Face Negotiations": 0.154,
                "In-Person Product Trials / Meetings": 0.128,
                "Third-Party Meetings": 0.179,
                "Proposal via Email/Online Portal": 0.179,
                "Online Product Demos": 0.154,
                "ROI Calculators": 0.205,
            },
            "Industry Awards/Recognition": {
                "Face-to-Face Negotiations": 0.162,
                "In-Person Product Trials / Meetings": 0.135,
                "Third-Party Meetings": 0.216,
                "Proposal via Email/Online Portal": 0.162,
                "Online Product Demos": 0.135,
                "ROI Calculators": 0.189,
            },
            "Office/Facility Tours": {
                "Face-to-Face Negotiations": 0.184,
                "In-Person Product Trials / Meetings": 0.211,
                "Third-Party Meetings": 0.158,
                "Proposal via Email/Online Portal": 0.184,
                "Online Product Demos": 0.132,
                "ROI Calculators": 0.132,
            },
            "Website": {
                "Face-to-Face Negotiations": 0.132,
                "In-Person Product Trials / Meetings": 0.132,
                "Third-Party Meetings": 0.132,
                "Proposal via Email/Online Portal": 0.158,
                "Online Product Demos": 0.211,
                "ROI Calculators": 0.237,
            },
            "Online Demos/Virtual Consultations": {
                "Face-to-Face Negotiations": 0.140,
                "In-Person Product Trials / Meetings": 0.163,
                "Third-Party Meetings": 0.140,
                "Proposal via Email/Online Portal": 0.163,
                "Online Product Demos": 0.209,
                "ROI Calculators": 0.186,
            },
            "Customer Reviews/Testimonials": {
                "Face-to-Face Negotiations": 0.175,
                "In-Person Product Trials / Meetings": 0.150,
                "Third-Party Meetings": 0.200,
                "Proposal via Email/Online Portal": 0.175,
                "Online Product Demos": 0.150,
                "ROI Calculators": 0.150,
            },
            "Comparison Tools": {
                "Face-to-Face Negotiations": 0.122,
                "In-Person Product Trials / Meetings": 0.146,
                "Third-Party Meetings": 0.146,
                "Proposal via Email/Online Portal": 0.171,
                "Online Product Demos": 0.195,
                "ROI Calculators": 0.220,
            },
            "Retargeting Ads": {
                "Face-to-Face Negotiations": 0.162,
                "In-Person Product Trials / Meetings": 0.135,
                "Third-Party Meetings": 0.135,
                "Proposal via Email/Online Portal": 0.162,
                "Online Product Demos": 0.216,
                "ROI Calculators": 0.189,
            },
            "Interactive Product Configurators": {
                "Face-to-Face Negotiations": 0.132,
                "In-Person Product Trials / Meetings": 0.158,
                "Third-Party Meetings": 0.158,
                "Proposal via Email/Online Portal": 0.132,
                "Online Product Demos": 0.211,
                "ROI Calculators": 0.211,
            },
            "Interactive FAQ or AI Chatbots": {
                "Face-to-Face Negotiations": 0.158,
                "In-Person Product Trials / Meetings": 0.132,
                "Third-Party Meetings": 0.132,
                "Proposal via Email/Online Portal": 0.184,
                "Online Product Demos": 0.184,
                "ROI Calculators": 0.211,
            },
        },
        "decision_making_to_purchase": {
            "Face-to-Face Negotiations": {
                "Face-to-Face Contract Signing": 0.1731,
                "Product/Service Handover Meeting": 0.1346,
                "Onsite Delivery or Setup": 0.1538,
                "E-commerce/Ordering Portals": 0.1154,
                "E-invoicing": 0.0962,
                "Dynamic Pricing Tools": 0.0962,
                "Custom Payment Portals": 0.1154,
                "Purchase Confirmation Emails": 0.1154,
            },
            "In-Person Product Trials / Meetings": {
                "Face-to-Face Contract Signing": 0.1429,
                "Product/Service Handover Meeting": 0.1607,
                "Onsite Delivery or Setup": 0.1607,
                "E-commerce/Ordering Portals": 0.125,
                "E-invoicing": 0.0893,
                "Dynamic Pricing Tools": 0.0893,
                "Custom Payment Portals": 0.1071,
                "Purchase Confirmation Emails": 0.125,
            },
            "Third-Party Meetings": {
                "Face-to-Face Contract Signing": 0.1702,
                "Product/Service Handover Meeting": 0.1277,
                "Onsite Delivery or Setup": 0.1277,
                "E-commerce/Ordering Portals": 0.1064,
                "E-invoicing": 0.1064,
                "Dynamic Pricing Tools": 0.1277,
                "Custom Payment Portals": 0.1064,
                "Purchase Confirmation Emails": 0.1277,
            },
            "Proposal via Email/Online Portal": {
                "Face-to-Face Contract Signing": 0.1034,
                "Product/Service Handover Meeting": 0.1207,
                "Onsite Delivery or Setup": 0.1034,
                "E-commerce/Ordering Portals": 0.1379,
                "E-invoicing": 0.1379,
                "Dynamic Pricing Tools": 0.1207,
                "Custom Payment Portals": 0.1379,
                "Purchase Confirmation Emails": 0.1379,
            },
            "Online Product Demos": {
                "Face-to-Face Contract Signing": 0.1094,
                "Product/Service Handover Meeting": 0.125,
                "Onsite Delivery or Setup": 0.1094,
                "E-commerce/Ordering Portals": 0.1406,
                "E-invoicing": 0.1094,
                "Dynamic Pricing Tools": 0.125,
                "Custom Payment Portals": 0.1406,
                "Purchase Confirmation Emails": 0.1406,
            },
            "ROI Calculators": {
                "Face-to-Face Contract Signing": 0.0968,
                "Product/Service Handover Meeting": 0.1129,
                "Onsite Delivery or Setup": 0.0968,
                "E-commerce/Ordering Portals": 0.1452,
                "E-invoicing": 0.129,
                "Dynamic Pricing Tools": 0.1452,
                "Custom Payment Portals": 0.1452,
                "Purchase Confirmation Emails": 0.129,
            },
        },
        "purchase_to_service": {
            "Face-to-Face Contract Signing": {
                "Maintenance Visits": 0.225,
                "Dedicated Account Manager": 0.2,
                "Help Desk/Support Portal": 0.175,
                "Online Training/Webinars": 0.15,
                "Video Tutorials": 0.125,
                "Live Chat/Chatbots for Support": 0.125
            },
            "Product/Service Handover Meeting": {
                "Maintenance Visits": 0.190,
                "Dedicated Account Manager": 0.214,
                "Help Desk/Support Portal": 0.167,
                "Online Training/Webinars": 0.143,
                "Video Tutorials": 0.143,
                "Live Chat/Chatbots for Support": 0.143
            },
            "Onsite Delivery or Setup": {
                "Maintenance Visits": 0.214,
                "Dedicated Account Manager": 0.167,
                "Help Desk/Support Portal": 0.190,
                "Online Training/Webinars": 0.143,
                "Video Tutorials": 0.143,
                "Live Chat/Chatbots for Support": 0.143
            },
            "E-commerce/Ordering Portals": {
                "Maintenance Visits": 0.136,
                "Dedicated Account Manager": 0.114,
                "Help Desk/Support Portal": 0.182,
                "Online Training/Webinars": 0.205,
                "Video Tutorials": 0.182,
                "Live Chat/Chatbots for Support": 0.182
            },
            "E-invoicing": {
                "Maintenance Visits": 0.128,
                "Dedicated Account Manager": 0.154,
                "Help Desk/Support Portal": 0.179,
                "Online Training/Webinars": 0.179,
                "Video Tutorials": 0.179,
                "Live Chat/Chatbots for Support": 0.179
            },
            "Dynamic Pricing Tools": {
                "Maintenance Visits": 0.114,
                "Dedicated Account Manager": 0.136,
                "Help Desk/Support Portal": 0.182,
                "Online Training/Webinars": 0.205,
                "Video Tutorials": 0.182,
                "Live Chat/Chatbots for Support": 0.182
            },
            "Custom Payment Portals": {
                "Maintenance Visits": 0.111,
                "Dedicated Account Manager": 0.156,
                "Help Desk/Support Portal": 0.200,
                "Online Training/Webinars": 0.178,
                "Video Tutorials": 0.156,
                "Live Chat/Chatbots for Support": 0.200
            },
            "Purchase Confirmation Emails": {
                "Maintenance Visits": 0.116,
                "Dedicated Account Manager": 0.140,
                "Help Desk/Support Portal": 0.163,
                "Online Training/Webinars": 0.186,
                "Video Tutorials": 0.186,
                "Live Chat/Chatbots for Support": 0.209
            },
        },
        "service_to_loyalty": {
            "Maintenance Visits": {
                "Loyalty Programs (Physical Rewards)": 0.1077,
                "Customer Appreciation Events": 0.1231,
                "Physical Awards/Recognition": 0.0923,
                "Branded Gifting Programs": 0.1077,
                "Subscription Services (Digital Renewal)": 0.0769,
                "Automated Personalization": 0.0923,
                "Automated Renewal Reminders": 0.0769,
                "Exclusive Access to Content": 0.0923,
                "Loyalty Emails/Discount Offers": 0.1231,
                "Gamified Loyalty Programs": 0.1077,
            },
            "Dedicated Account Manager": {
                "Loyalty Programs (Physical Rewards)": 0.1081,
                "Customer Appreciation Events": 0.1216,
                "Physical Awards/Recognition": 0.0946,
                "Branded Gifting Programs": 0.0946,
                "Subscription Services (Digital Renewal)": 0.0811,
                "Automated Personalization": 0.0946,
                "Automated Renewal Reminders": 0.0946,
                "Exclusive Access to Content": 0.1081,
                "Loyalty Emails/Discount Offers": 0.1081,
                "Gamified Loyalty Programs": 0.0946,
            },
            "Help Desk/Support Portal": {
                "Loyalty Programs (Physical Rewards)": 0.0822,
                "Customer Appreciation Events": 0.0685,
                "Physical Awards/Recognition": 0.0959,
                "Branded Gifting Programs": 0.0822,
                "Subscription Services (Digital Renewal)": 0.1096,
                "Automated Personalization": 0.0959,
                "Automated Renewal Reminders": 0.1233,
                "Exclusive Access to Content": 0.1096,
                "Loyalty Emails/Discount Offers": 0.1096,
                "Gamified Loyalty Programs": 0.1233,
            },
            "Online Training/Webinars": {
                "Loyalty Programs (Physical Rewards)": 0.0704,
                "Customer Appreciation Events": 0.0845,
                "Physical Awards/Recognition": 0.0845,
                "Branded Gifting Programs": 0.0704,
                "Subscription Services (Digital Renewal)": 0.1268,
                "Automated Personalization": 0.1127,
                "Automated Renewal Reminders": 0.1268,
                "Exclusive Access to Content": 0.1127,
                "Loyalty Emails/Discount Offers": 0.0986,
                "Gamified Loyalty Programs": 0.1127,
            },
            "Video Tutorials": {
                "Loyalty Programs (Physical Rewards)": 0.0896,
                "Customer Appreciation Events": 0.0746,
                "Physical Awards/Recognition": 0.0746,
                "Branded Gifting Programs": 0.0896,
                "Subscription Services (Digital Renewal)": 0.1343,
                "Automated Personalization": 0.1045,
                "Automated Renewal Reminders": 0.1194,
                "Exclusive Access to Content": 0.1194,
                "Loyalty Emails/Discount Offers": 0.1045,
                "Gamified Loyalty Programs": 0.0896,
            },
            "Live Chat/Chatbots for Support": {
                "Loyalty Programs (Physical Rewards)": 0.0833,
                "Customer Appreciation Events": 0.0694,
                "Physical Awards/Recognition": 0.0694,
                "Branded Gifting Programs": 0.0833,
                "Subscription Services (Digital Renewal)": 0.1250,
                "Automated Personalization": 0.1250,
                "Automated Renewal Reminders": 0.1111,
                "Exclusive Access to Content": 0.1111,
                "Loyalty Emails/Discount Offers": 0.0972,
                "Gamified Loyalty Programs": 0.1250,
            },
        },
        "loyalty_to_ambassador": {
            "Loyalty Programs (Physical Rewards)": {
                "Referral Program (Physical Rewards)": 0.2045,
                "Customer Advisory Board (In-Person Meetings)": 0.1818,
                "Invitations to Product Launches or Corporate Events": 0.1818,
                "Referral Program (Digital Rewards)": 0.1591,
                "Social Media Sharing": 0.1364,
                "Affiliate or Influencer Partnerships": 0.1364,
            },
            "Customer Appreciation Events": {
                "Referral Program (Physical Rewards)": 0.1702,
                "Customer Advisory Board (In-Person Meetings)": 0.1915,
                "Invitations to Product Launches or Corporate Events": 0.1915,
                "Referral Program (Digital Rewards)": 0.1702,
                "Social Media Sharing": 0.1277,
                "Affiliate or Influencer Partnerships": 0.1489,
            },
            "Physical Awards/Recognition": {
                "Referral Program (Physical Rewards)": 0.1795,
                "Customer Advisory Board (In-Person Meetings)": 0.2051,
                "Invitations to Product Launches or Corporate Events": 0.1538,
                "Referral Program (Digital Rewards)": 0.1795,
                "Social Media Sharing": 0.1282,
                "Affiliate or Influencer Partnerships": 0.1538,
            },
            "Branded Gifting Programs": {
                "Referral Program (Physical Rewards)": 0.1837,
                "Customer Advisory Board (In-Person Meetings)": 0.1429,
                "Invitations to Product Launches or Corporate Events": 0.1633,
                "Referral Program (Digital Rewards)": 0.1837,
                "Social Media Sharing": 0.1633,
                "Affiliate or Influencer Partnerships": 0.1633,
            },
            "Subscription Services (Digital Renewal)": {
                "Referral Program (Physical Rewards)": 0.1333,
                "Customer Advisory Board (In-Person Meetings)": 0.1556,
                "Invitations to Product Launches or Corporate Events": 0.1333,
                "Referral Program (Digital Rewards)": 0.2,
                "Social Media Sharing": 0.2,
                "Affiliate or Influencer Partnerships": 0.1778,
            },
            "Automated Personalization": {
                "Referral Program (Physical Rewards)": 0.1304,
                "Customer Advisory Board (In-Person Meetings)": 0.1522,
                "Invitations to Product Launches or Corporate Events": 0.1522,
                "Referral Program (Digital Rewards)": 0.1739,
                "Social Media Sharing": 0.1957,
                "Affiliate or Influencer Partnerships": 0.1957,
            },
            "Automated Renewal Reminders": {
                "Referral Program (Physical Rewards)": 0.1190,
                "Customer Advisory Board (In-Person Meetings)": 0.1190,
                "Invitations to Product Launches or Corporate Events": 0.1429,
                "Referral Program (Digital Rewards)": 0.2143,
                "Social Media Sharing": 0.2143,
                "Affiliate or Influencer Partnerships": 0.1905,
            },
            "Exclusive Access to Content": {
                "Referral Program (Physical Rewards)": 0.1489,
                "Customer Advisory Board (In-Person Meetings)": 0.1277,
                "Invitations to Product Launches or Corporate Events": 0.1915,
                "Referral Program (Digital Rewards)": 0.1702,
                "Social Media Sharing": 0.1915,
                "Affiliate or Influencer Partnerships": 0.1702,
            },
            "Loyalty Emails/Discount Offers": {
                "Referral Program (Physical Rewards)": 0.1395,
                "Customer Advisory Board (In-Person Meetings)": 0.1395,
                "Invitations to Product Launches or Corporate Events": 0.1628,
                "Referral Program (Digital Rewards)": 0.1860,
                "Social Media Sharing": 0.2093,
                "Affiliate or Influencer Partnerships": 0.1628,
            },
            "Gamified Loyalty Programs": {
                "Referral Program (Physical Rewards)": 0.1633,
                "Customer Advisory Board (In-Person Meetings)": 0.1224,
                "Invitations to Product Launches or Corporate Events": 0.1633,
                "Referral Program (Digital Rewards)": 0.1837,
                "Social Media Sharing": 0.1837,
                "Affiliate or Influencer Partnerships": 0.1837,
            },
        },
    }
    pass
