from flask import Flask, request, render_template, jsonify
from calculator.operations import add, subtract, multiply, divide

app = Flask(__name__)


@app.route("/", methods=["GET"])
def main():
    return render_template("index.html")


@app.route("/math", methods=["POST"])
def math():
    try:
        data = request.get_json()

        num1 = data["num1"]
        num2 = data["num2"]
        operation = data["operation"]

        if operation == "add":
            result = add(num1, num2)

        elif operation == "subtract":
            result = subtract(num1, num2)

        elif operation == "multiply":
            result = multiply(num1, num2)

        elif operation == "divide":
            result = divide(num1, num2)

        else:
            return jsonify({"error": "Invalid operation"}), 400

        return jsonify({"result" : result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
