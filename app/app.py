from flask import Flask, render_template, request, redirect, url_for, session
from backend.objects.inputObj import InputFields
from backend.segmentation.macroSeg import MacroClusteringModel
from backend.objects.macroObj import MacroSegmentation
from backend.segmentation.microSeg import MicroClusteringModel
from backend.objects.microObj import MicroSegmentation
from backend.segmentation.journeySeg import CustomerJourneyModel

app = Flask(__name__)
app.secret_key = '123'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/input', methods=['GET', 'POST'])
def input_page():
    if request.method == 'POST':
        input = InputFields(
            industry=request.form.get('industry_input')
            , location=request.form.getlist('location_input')
            , organization_size=request.form.get('size_input')
            , annual_revenue=request.form.get('annual_revenue_input')
            , geographical_focus=request.form.get('geo_focus_input')
            , strategic_positioning=request.form.getlist('strategic_position_input'))

        input.set_name = request.form.get('company_name_input')
        input.set_competitors = request.form.get('key_competitors_input')
        session['input'] = {
            'industry': input.industry,
            'location': input.location,
            'organization_size': input.organization_size,
            'annual_revenue': input.annual_revenue,
            'geographical_focus': input.geographical_focus,
            'strategic_positioning': input.strategic_positioning,
            'name': input.set_name,
            'competitors': input.set_competitors
        }

        return redirect(url_for('macro_segmentation'))

    return render_template('Input.html')


@app.route('/macro_segmentation')
def macro_segmentation():
    input_data = session.get('input')
    input_object = InputFields(
        industry=input_data['industry'],
        location=input_data['location'],
        organization_size=input_data['organization_size'],
        annual_revenue=input_data['annual_revenue'],
        geographical_focus=input_data['geographical_focus'],
        strategic_positioning=input_data['strategic_positioning'],
    )
    input_object.set_name(input_data.get('name'))
    input_object.set_competitors(input_data.get('competitors'))
    macro_object = MacroClusteringModel.load_and_predict("models/macroModel.joblib", input_object)
    filtered_data = [
        {
            "industry": obj.industry,
            "organization_size": obj.organization_size,
            "annual_revenue": obj.annual_revenue,
            "operational_regions": obj.operational_regions,
            "market_density": obj.market_density,
            "purchasing_frequency": obj.purchasing_frequency,
            "purchasing_volume": obj.purchasing_volume,
            "technology_adoption": obj.technology_adoption,
            "usage_engagement_rate": obj.usage_engagement_rate,
            "ownership_structure": obj.ownership_structure,
            "growth_stage": obj.growth_stage,
            "influence_structure": obj.influence_structure,
        }
        for obj in macro_object
    ]

    return render_template('macro_segmentation.html', macro_object=filtered_data)


@app.route('/decision_makers', methods=['POST'])
def decision_makers():
    def sanitize(value):
        if isinstance(value, str):
            return value.replace("'s", " ")
        return value

    selected_data = request.form.to_dict()

    selected_macro = MacroSegmentation(
        input_fields=None,
        industry=selected_data.get('industry'),
        organization_size=selected_data.get('organization_size'),
        annual_revenue=selected_data.get('annual_revenue'),
        operational_regions=selected_data.get('operational_regions'),
        market_density=selected_data.get('market_density'),
        purchasing_frequency=selected_data.get('purchasing_frequency'),
        purchasing_volume=selected_data.get('purchasing_volume'),
        technology_adoption=selected_data.get('technology_adoption'),
        usage_engagement_rate=selected_data.get('usage_engagement_rate'),
        ownership_structure=selected_data.get('ownership_structure'),
        growth_stage=selected_data.get('growth_stage'),
        influence_structure=selected_data.get('influence_structure')
    )

    top_micro_objects = MicroClusteringModel.load_and_predict("models/microModel.joblib", selected_macro)

    # Sanitize all micro object data
    sanitized_micro_objects = [
        {key: sanitize(value) for key, value in vars(micro).items()} for micro in top_micro_objects
    ]

    return render_template('decision_makers.html', data=selected_data, top_micro_objects=sanitized_micro_objects)


@app.route('/touch_points', methods=['POST'])
def touch_points():
    selected_micro_data = request.form.to_dict()
    selected_micro = MicroSegmentation(
        macro_segmentation=None,
        age=selected_micro_data.get('age'),
        gender=selected_micro_data.get('gender'),
        education_level=selected_micro_data.get('education_level'),
        technology_used=selected_micro_data.get('technology_used'),

        job_title=selected_micro_data.get('job_title'),
        experience_level=selected_micro_data.get('experience_level'),
        functional_field=selected_micro_data.get('functional_field'),
        decision_making_role=selected_micro_data.get('decision_making_role'),
        work_environment=selected_micro_data.get('work_environment'),
        professional_network=selected_micro_data.get('professional_network'),

        risk_tolerance=selected_micro_data.get('risk_tolerance'),
        decision_making_style=selected_micro_data.get('decision_making_style'),
        motivations=selected_micro_data.get('motivations'),
        personality_traits=selected_micro_data.get('personality_traits'),
        pain_points=selected_micro_data.get('pain_points'),

        kpis=selected_micro_data.get('kpis'),

        challenges=selected_micro_data.get('challenges'),

        goals=selected_micro_data.get('goals'),

    )

    # Pass the selected microdata to a model for prediction
    customer_journey = CustomerJourneyModel.load_and_predict(
        "models/customerjourneyModel.joblib",
        selected_micro
    )


    return render_template('touch_points.html', data=selected_micro_data, customer_journey=customer_journey)


@app.route('/final_report')
def final_report():
    return render_template('final_report.html')


def runApp():
    app.run(host='0.0.0.0', port=5000)
