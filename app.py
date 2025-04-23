from flask import Flask, request, render_template , jsonify# type: ignore

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    num1 = float(request.json['num1'])
    num2 = float(request.json['num2'])
    operation = request.json['operation']
    if operation == 'add':
        result = num1 + num2
    elif operation == 'subtract':
        result = num1 - num2
    elif operation == 'multiply':
        result = num1 * num2
    elif operation == 'divide':
        if num2 != 0:
            result = num1 / num2
        else:
            result = 'Error: Division by zero'
    else:
        result = 'Error: Invalid operation'

    return jsonify({'result': result})
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)
