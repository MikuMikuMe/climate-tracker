Creating a complete Python program for a web application like `climate-tracker` involves setting up a basic web framework, reading environmental data, and potentially visualizing trends. For simplicity, I'll use Flask for the web framework, Pandas for data handling, and Matplotlib for visualization. This basic implementation will include error handling and comments to guide you through the code. 

Before starting, ensure you have the necessary Python packages installed. You can usually install them using pip:

```bash
pip install flask pandas matplotlib
```

Below is a basic implementation of `climate-tracker`:

```python
from flask import Flask, render_template, request, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import os
from io import BytesIO
import base64

app = Flask(__name__)

# Load your climate data
def load_data():
    try:
        # Assume 'climate_data.csv' is your dataset
        data = pd.read_csv('climate_data.csv')
        return data
    except FileNotFoundError:
        raise Exception("Data file not found. Please ensure 'climate_data.csv' exists.")
    except pd.errors.EmptyDataError:
        raise Exception("Data file is empty. Please provide a valid data file.")

# Helper function to generate plots
def plot_data(data):
    plt.figure(figsize=(10, 6))
    plt.plot(data['Year'], data['Temperature'], marker='o')
    plt.title('Temperature Changes Over Years')
    plt.xlabel('Year')
    plt.ylabel('Temperature (°C)')
    plt.grid(True)
    
    # Save the plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    
    # Encode the image to base64 to embed it in HTML
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url

@app.route('/')
def index():
    try:
        # Load climate data
        data = load_data()

        # Check if the necessary columns are present
        if 'Year' not in data.columns or 'Temperature' not in data.columns:
            raise Exception("Data file format is incorrect. Columns 'Year' and 'Temperature' are required.")
    
        # Render plot
        plot_url = plot_data(data)

        # Render the main page
        return render_template('index.html', plot_url=plot_url)
    except Exception as e:
        return f"Error: {e}"

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        data = load_data()
        return jsonify(data.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Debug should be False in a production environment
    app.run(debug=True)
```

### `templates/index.html`

Create a folder named `templates` in the same directory as your Python script, then create an `index.html` file:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Climate Tracker</title>
</head>
<body>
    <h1>Climate Tracker</h1>
    <img src="data:image/png;base64,{{ plot_url }}" alt="Climate Data Plot" />
</body>
</html>
```

### Error Handling

1. **File Loading**: Checks if the CSV file is missing or empty, and reports relevant errors.
2. **Data Integrity**: Validates the presence of expected columns in the data.
3. **Web Requests**: Catches exceptions and returns appropriate error messages.

### Running the Application

1. Save the Python script with an appropriate name (e.g., `app.py`).
2. Prepare a `climate_data.csv` file with `Year` and `Temperature` columns in the same directory.
3. Run the application:

   ```bash
   python app.py
   ```

4. Open a web browser and navigate to `http://127.0.0.1:5000/` to view the application.

This example provides a basic scaffold for the `climate-tracker` application. For a more sophisticated application, you might want to integrate more features, use a database for data storage, and add more robust data processing and visualization tools.