from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route('/p', methods=['GET'])
def get_prime():
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    return jsonify({"number": random.choice(primes)})

@app.route('/f', methods=['GET'])
def get_fibonacci():
    fibonaccis = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    return jsonify({"number": random.choice(fibonaccis)})

@app.route('/e', methods=['GET'])
def get_even():
    evens = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    return jsonify({"number": random.choice(evens)})

@app.route('/r', methods=['GET'])
def get_random():
    return jsonify({"number": random.randint(1, 100)})

if __name__ == '__main__':
    app.run(port=5001)
