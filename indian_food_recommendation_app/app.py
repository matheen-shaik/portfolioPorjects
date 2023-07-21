from flask import Flask, render_template, request
from indian_food import IndianFoodRecommendation, InvalidTypeException, InvalidCoreException

class InvalidTypeException(Exception):
    pass

class InvalidCoreException(Exception):
    pass

app = Flask(__name__)
recommendation_system = IndianFoodRecommendation()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    food_type = request.form.get('type')  # Use request.form.get() to retrieve selected option
    specifications = request.form.get('specifications')  # Use request.form.get() to retrieve selected option
    core = request.form.getlist('core')  # Use request.form.getlist() to retrieve multiple selected options

    try:
        recommendations, surprise = recommendation_system.food_recommendation(food_type, specifications, core)
        return render_template('recommendations.html', recommendations=recommendations, surprise=surprise)
    except (InvalidTypeException, InvalidCoreException) as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
