from flask import Flask, render_template, request
import Testing # Replace with the name of your script file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script', methods=['POST'])
def run_script():
    Testing.main()  # Replace with the actual function to run your script
    return "Script has been run!"

if __name__ == '__main__':
    app.run()
