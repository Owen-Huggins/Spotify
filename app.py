from flask import Flask, render_template, request
import Testing # Replace with the correct name and location of your script file
import os
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script', methods=['POST'])
def run_script():
    Testing.main()  # Replace with the actual function to run your script
    return "Script has been run!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    app.run()
