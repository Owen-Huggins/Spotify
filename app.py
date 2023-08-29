from flask import Flask, render_template, request
import SpotifyApplication.Testing # Replace with the correct name and location of your script file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script', methods=['POST'])
def run_script():
    SpotifyApplication.Testing.main()  # Replace with the actual function to run your script
    return "Script has been run!"

if __name__ == '__main__':
    app.run()