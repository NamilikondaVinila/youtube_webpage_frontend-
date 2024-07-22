from flask import Flask, jsonify
import requests

app = Flask(__name__)

WINDOW_SIZE = 10
STORED_NUMBERS = []

ENDPOINTS = {
    'prime': 'http://20.244.56.144/test/primes',
    'fibo': 'http://20.244.56.144/test/fibo',
    'even': 'http://20.244.56.144/test/even',
    'random': 'http://20.244.56.144/test/rand'
}

def fetch(numtype):
    try:
        response = requests.get(ENDPOINTS[numtype], timeout=0.5)
        response.raise_for_status()
        data = response.json()
        return data.get('numbers', [])
    except requests.exceptions.Timeout:
        print(f"Request to {ENDPOINTS[numtype]} timed out.")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Request to {ENDPOINTS[numtype]} failed: {e}")
        return []

def calculate_average(numbers):
    return sum(numbers) / len(numbers) if numbers else 0

@app.route('/numbers/<string:numberid>', methods=['GET'])
def get_numbers(numberid):
    if numberid not in ENDPOINTS:
        return jsonify({'error': 'Invalid number ID'}), 400

    fetched_numbers = fetch(numberid)

    global STORED_NUMBERS
    window_prev_state = STORED_NUMBERS.copy()

    for num in fetched_numbers:
        if num not in STORED_NUMBERS:
            STORED_NUMBERS.append(num)
        if len(STORED_NUMBERS) > WINDOW_SIZE:
            STORED_NUMBERS.pop(0)

    window_curr_state = STORED_NUMBERS.copy()
    avg = calculate_average(STORED_NUMBERS)

    response = {
        'windowPrevState': window_prev_state,
        'windowCurrState': window_curr_state,
        'numbers': fetched_numbers,
        'avg': avg
    }
    
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9876)
