const display = document.getElementById("display");
const expression = document.getElementById("expression");

let currentInput = "0";
let firstNumber = null;
let operation = null;
let waitingForSecondNumber = false;

/* --------------------
Update display
-------------------- */

function updateDisplay() {
    display.textContent = currentInput;
}

/* --------------------
Number input
-------------------- */

function inputNumber(number) {

    if (waitingForSecondNumber) {
        currentInput = number;
        waitingForSecondNumber = false;
        updateDisplay();
        return;
    }

    if (number === "." && currentInput.includes(".")) {
        return;
    }

    if (currentInput === "0" && number !== ".") {
        currentInput = number;
    } else {
        currentInput += number;
    }

    updateDisplay();

}

/* --------------------
Operation
-------------------- */

function chooseOperation(selectedOperation) {

    const inputValue = parseFloat(currentInput);

    if (firstNumber === null) {
        firstNumber = inputValue;
    } else if (!waitingForSecondNumber) {
        calculate();
    }

    operation = selectedOperation;
    waitingForSecondNumber = true;

    expression.textContent =
        `${firstNumber} ${getOperationSymbol(operation)}`;

}

/* --------------------
Calculate
-------------------- */

async function calculate() {

    if (firstNumber === null || operation === null) {
        return;
    }

    const secondNumber = parseFloat(currentInput);

    const data = {
        num1: firstNumber,
        num2: secondNumber,
        operation: operation
    }

    try {

        const response = await fetch("/math", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(data)
        });
        
        const api_response = await response.json();

        if (!response.ok) {
            display.textContent = result.error || "Error";
            return;
        }

        expression.textContent =
            `${firstNumber} ${getOperationSymbol(operation)} ${secondNumber} =`;
    
        currentInput = String(api_response.result);
    
        firstNumber = null;
        operation = null;
        waitingForSecondNumber = true;
    
        updateDisplay();

    } catch (error) {

        console.error("Calculator API error:", error);

        display.textContent = "Error";
    }

}

/* --------------------
Clear
-------------------- */

function clearCalculator() {

    currentInput = "0";
    firstNumber = null;
    operation = null;
    waitingForSecondNumber = false;

    expression.textContent = "";

    updateDisplay();

}

/* --------------------
Backspace
-------------------- */

function backspace() {

    if (waitingForSecondNumber) {
        return;
    }

    if (currentInput.length === 1) {
        currentInput = "0";
    } else {
        currentInput = currentInput.slice(0, -1);
    }

    updateDisplay();

}

/* --------------------
Percentage
-------------------- */

function percentage() {

    const value = parseFloat(currentInput);

    currentInput = String(value / 100);

    updateDisplay();

}

/* --------------------
Operation symbols
-------------------- */

function getOperationSymbol(operation) {

    switch (operation) {

        case "add":
            return "+";

        case "subtract":
            return "−";

        case "multiply":
            return "×";

        case "divide":
            return "÷";
    }

}

/* --------------------
Button events
-------------------- */

document.querySelectorAll(".number").forEach(button => {

    button.addEventListener("click", () => {

        inputNumber(button.dataset.number);

    });

});

document.querySelectorAll(".operator").forEach(button => {

    button.addEventListener("click", () => {

        chooseOperation(button.dataset.operation);

    });

});

document
    .querySelector('[data-action="calculate"]')
    .addEventListener("click", calculate);

document
    .querySelector('[data-action="clear"]')
    .addEventListener("click", clearCalculator);

document
    .querySelector('[data-action="backspace"]')
    .addEventListener("click", backspace);

document
    .querySelector('[data-action="percent"]')
    .addEventListener("click", percentage);

/* --------------------
Keyboard support
-------------------- */

document.addEventListener("keydown", event => {

    if (
        event.key >= "0" &&
        event.key <= "9"
    ) {
        inputNumber(event.key);
    }

    else if (event.key === ".") {
        inputNumber(".");
    }

    else if (event.key === "+") {
        chooseOperation("add");
    }

    else if (event.key === "-") {
        chooseOperation("subtract");
    }

    else if (event.key === "*") {
        chooseOperation("multiply");
    }

    else if (event.key === "/") {
        chooseOperation("divide");
    }

    else if (event.key === "Enter" || event.key === "=") {
        calculate();
    }

    else if (event.key === "Backspace") {
        backspace();
    }

    else if (event.key === "Escape") {
        clearCalculator();
    }

});