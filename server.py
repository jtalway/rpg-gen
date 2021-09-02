from flask import Flask, render_template, url_for, request, redirect
import csv
from critical import *
from fumble import *
from abilityscore import *
import random

app = Flask(__name__)


@app.route('/')
@app.route('/home')
@app.route('/index')
@app.route('/index.html')
def my_home():
	return render_template('index.html')

@app.route('/critical')
@app.route('/criticals')
@app.route('/criticalhit')
def critical():
    return render_template('critical.html')

@app.route('/fumble')
@app.route('/fumbles')
def fumble():
    return render_template('fumble.html')

def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        file = database.write(f'\n{email}, {subject}, {message}')

def write_to_csv(data):
    with open('database.csv', newline='', mode='a') as database2:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            return redirect('thankyou.html')
        except:
            return '[-] Did not save to database'
    else:
        return 'something went wrong, try again!'

# CRITICALS
@app.route('/generate_critical', methods=['POST', 'GET'])
def generate_critical():
    if request.method == 'POST':
        weaponDmg = request.form['weaponDmg']
        selected = request.form.getlist('severity')
        severity = selected.count('1')
        total_severity = int(weaponDmg) + severity
        crit_array = severity_gen(total_severity)
        critical_effects = crit_gen(crit_array)
        # check for duplicate results and add/multiply numeric values
        return render_template('critical.html', critical_effects = critical_effects)
    else:
        return 'something went wrong, try again!'

# FUMBLES
@app.route('/generate_fumble', methods=['POST', 'GET'])
def generate_fumble():
    if request.method == 'POST':
        proficient = request.form['proficient']
        # if non-proficient there MUST be a result
        # get list of deductions from fsev criteria on form
        selected = request.form.getlist('fsev')
        # calculate number of reductions
        fseverity = selected.count('1')
        # get number of fumble severity from file by random roll
        fsev_result = fseverity_gen()
        # convert result into a list 
        convert_fsev = int(fsev_result) * ['fumble']
        prelim_fumble_effects = fsev_gen(convert_fsev)
        reduce_fumble_effects = int(proficient) + fseverity
        if reduce_fumble_effects >= len(prelim_fumble_effects):
            fumble_effects = ['No Results']
        elif reduce_fumble_effects < len(prelim_fumble_effects):
            x = len(prelim_fumble_effects) - reduce_fumble_effects
            fumble_effects = random.choices(prelim_fumble_effects, k=x)
        else:
            return 'something is amiss'

        # check for duplicate results and add/multiply numeric values
        return render_template('fumble.html', fumble_effects = fumble_effects)
    else:
        return 'something went wrong, try again!'

# ABILITY SCORES
@app.route('/generate_abilityscore', methods=['POST', 'GET'])
def generate_abilityscore():
    if request.method == 'POST':
        method = request.form['abilityscoremethod']
        ability_scores = abilityscore_gen(method)
        return render_template('abilityscore.html', ability_scores = ability_scores)
    else:
        return 'something went wrong, try again!'

# @app.errorhandler(404)
# def not_found():
#     """Page not found."""
#     return make_response(
#         render_template("404.html"),
#         404
#      )


# @app.errorhandler(400)
# def bad_request():
#     """Bad request."""
#     return make_response(
#         render_template("400.html"),
#         400
#     )


# @app.errorhandler(500)
# def server_error():
#     """Internal server error."""
#     return make_response(
#         render_template("500.html"),
#         500
#     )

@app.route('/abilityscore')
def abilityscore():
     return generate_abilityscore()

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)