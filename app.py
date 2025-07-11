from flask import Flask, jsonify, request
from flask_cors import CORS
import fastf1
import pycountry

app = Flask(__name__)
CORS(app)

fastf1.Cache.enable_cache('cache')

# Helper function to get flag emoji from nationality
def nationality_to_flag(nationality):
    # Map nationality to ISO alpha_2 country code (common fixes)
    mapping = {
        'British': 'GB',
        'American': 'US',
        'Dutch': 'NL',
        'Monegasque': 'MC',
        'Russian': 'RU',
        'Korean': 'KR',
        'Thai': 'TH',
        'Chinese': 'CN',
        'Indonesian': 'ID',
        'Argentine': 'AR',
        'German': 'DE',
        'Spanish': 'ES',
        'Finnish': 'FI',
        'Australian': 'AU',
        'Canadian': 'CA',
        'French': 'FR',
        'Italian': 'IT',
        'Brazilian': 'BR',
        'Japanese': 'JP',
        'Mexican': 'MX',
        'Indian': 'IN',
        'Austrian': 'AT',
    }
    
    country_code = mapping.get(nationality, nationality)

    try:
        country = pycountry.countries.get(name=country_code)
        if country:
            country_code = country.alpha_2
    except:
        pass
    
    if len(country_code) == 2:
        return chr(ord(country_code[0].upper()) + 127397) + chr(ord(country_code[1].upper()) + 127397)
    return ''  # fallback no flag

@app.route('/race-standings')
def race_standings():
    year = request.args.get('year')
    gp = request.args.get('gp')

    missing_params = []
    if not year:
        missing_params.append('year')
    if not gp:
        missing_params.append('gp')

    if missing_params:
        return jsonify({
            'error': f'Missing mandatory parameter(s): {", ".join(missing_params)}. Please provide all required fields.'
        }), 400

    try:
        year = int(year)
    except ValueError:
        return jsonify({'error': 'Year must be an integer.'}), 400

    try:
        session = fastf1.get_session(year, gp, 'R')
        session.load()
    except Exception as e:
        return jsonify({'error': f'Failed to load session: {str(e)}'}), 400

    results = session.results

    standings = []
    for _, row in results.iterrows():
        standings.append({
            'Position': row['Position'],
            'DriverNumber': row['DriverNumber'],
            'BroadcastName': row['BroadcastName'],
            'Abbreviation': row['Abbreviation'],
            'Status': row['Status'],
            'Points': row['Points'],
            'Laps': row['Laps'],
            'TeamName': row['TeamName'],
            'Nationality': row['CountryCode'],  # This is the ISO country code actually
            'Flag': nationality_to_flag(row['CountryCode'])
        })

    return jsonify(standings)

if __name__ == '__main__':
    app.run(debug=True)
