from flask import Flask, render_template, url_for, request
import joblib
import sqlite3

# Load model and initialize Flask app
app = Flask(__name__)
try:
    random_forest = joblib.load('./models/randomforest.lb')
except FileNotFoundError:
    random_forest = None
    print("Model file not found. Ensure the model path is correct.")

data_insert_query = """
INSERT INTO project (age, gender, bmi, children, region, smoker, health, prediction)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
"""

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == "POST":
        try:
            # Retrieve form data
            region = request.form['region']
            children = int(request.form.get('children', 0))
            health = int(request.form.get('health', 0))
            smoker = int(request.form.get('smoker', 0))
            gender = int(request.form.get('gender', 0))
            weight = float(request.form.get('weight', 0))  # New field for weight
            height = float(request.form.get('height', 0))  # New field for height
            age = int(request.form.get('age', 0))

            # Calculate BMI
            if height > 0:
                bmi = weight / ((height / 100) ** 2)
            else:
                bmi = 0  # Default if height is zero to avoid division by zero

            # Encode region
            region_northeast = int(region == 'ne')
            region_northwest = int(region == 'nw')
            region_southeast = int(region == 'se')
            region_southwest = int(region == 'sw')

            # Prepare data for prediction
            unseen_data = [[age, gender, bmi, children, smoker, health,
                            region_northeast, region_northwest, region_southeast, region_southwest]]

            # Make prediction if model is loaded
            if random_forest:
                prediction = str(random_forest.predict(unseen_data)[0])
            else:
                prediction = "Model not available"

            # Insert data into database
            conn = sqlite3.connect('insurance.db')
            cur = conn.cursor()
            Data = (age, gender, bmi, children, region, smoker, health, prediction)
            cur.execute(data_insert_query, Data)
            conn.commit()

            print("Data inserted into database:", Data)
            return render_template('final.html', output=prediction)

        except Exception as e:
            print(f"Error occurred: {e}")
            return render_template('error.html', error_message=str(e))

        finally:
            if 'conn' in locals():
                conn.close()

    return render_template('project.html')

if __name__ == "__main__":
    app.run(debug=True)
