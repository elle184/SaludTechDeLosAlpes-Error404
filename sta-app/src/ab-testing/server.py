from flask import Flask

# Create a Flask application
app = Flask(__name__)

# Define a route for the root URL
@app.route('/', methods=['GET'])
def hello_world():
    return 'Hola mundo'

# Run the application when this file is executed directly
if __name__ == '__main__':
    # Running on port 5432, allowing external access
    app.run(host='0.0.0.0', port=5432, debug=True)