from flask import Flask, request, render_template, render_template_string
import logging
from gradio_client import Client
import os



# Initialize Flask app
app = Flask(__name__)

# Initialize Gradio Client
client = Client("PrudhviRajGandrothu/llama-3.1")

def generate_recommendation_prompt(criteria):
    climate = criteria.get('climate', '')
    soil = criteria.get('soil', '')
    sunlight = criteria.get('sunlight', '')
    space = criteria.get('space', '')
    preferences = criteria.get('preferences', '')
    maintenance = criteria.get('maintenance', '')
    allergies = criteria.get('allergies', '')
    availability = criteria.get('availability', '')
    environmental = criteria.get('environmental', '')
    growth_cycle = criteria.get('growth-cycle', '')

    prompt = (
        f"Recommend plants that are suitable for the following criteria in India.\n"
        f"Generate a list of at least 4 plants that match these criteria in HTML format:\n"
        f"Climate - {climate}\n"
        f"Soil - {soil}\n"
        f"Sunlight - {sunlight}\n"
        f"Space Available - {space} square meters\n"
        f"User Preferences - {preferences}\n"
        f"Maintenance Level - {maintenance}\n"
        f"Allergies - {allergies}\n"
        f"Availability - {availability}\n"
        f"Environmental Impact - {environmental}\n"
        f"Growth Cycle - {growth_cycle}\n\n"
        f"For each plant, provide the following details in HTML:\n"
        f"- Name (including scientific name)\n"
        f"- Caring Tips\n"
        f"- Growing Methods\n"
        f"- Water Schedules\n"
        f"- Ways to Grow\n"
        f"- Organic Methods\n"
        f"- Artificial Methods\n"
    )
    return prompt

@app.route('/recommend_by_criteria', methods=['POST'])
def recommend_by_criteria():
    criteria = request.form.to_dict()
    # Generate the prompt for Gradio Client
    prompt = generate_recommendation_prompt(criteria)

    # Call Gradio Client for recommendations
    try:
        result = client.predict(
            message=prompt,
            api_name="/chat"
        )
        recommendations_html = result.strip()

        # Render the recommendations as HTML
        return render_template_string(recommendations_html)

    except Exception as e:
        return render_template('index.html', error="Error retrieving plant suggestions. Please try again later.")

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use the port provided by Render
    app.run(host='0.0.0.0', port=port, debug=True)
