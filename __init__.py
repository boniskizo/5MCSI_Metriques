from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
from collections import Counter
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')
  
@app.route("/contact/")
def MaPremiereAPI():
    return render_template('contact.html')

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")

app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes = date_object.minute
        return jsonify({'minutes': minutes})

def get_commit_data():
    url = "https://api.github.com/repos/boniskizo/5MCSI_Metriques/commits"
    response = urlopen(url)
    raw_content = response.read()
    commits = json.loads(raw_content.decode('utf-8'))

    times = []
    for commit in commits:
        date_str = commit['commit']['author']['date']
        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        dt_min = dt.replace(second=0, microsecond=0)
        times.append(dt_min.strftime("%Y-%m-%d %H:%M"))

    counter = Counter(times)
    data = sorted(counter.items())
    return data

@app.route("/commits-data")
def commits_data():
    data = get_commit_data()
    return jsonify(data)

@app.route("/commits")
def commits():
    return render_template("afficheCommit.html")

if __name__ == "__main__":
  app.run(debug=True)
