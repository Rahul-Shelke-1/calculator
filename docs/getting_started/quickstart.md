# Quickstart Guide

Welcome to the project! This guide will help you get up and running in less than 5 minutes.

## 1. Prerequisites

Before installing, ensure you have the following requirements met:
* **Python 3.11+** (or your language version)
* **uv** package manager

## 2. Installation

Install the package via `uv` from PyPI:

```bash
uv add -r requirements.txt 
```

Alternatively, you can clone the repository and install it locally:

```bash
git clone https://github.com/Rahul-Shelke-1/calculator.git
cd calculator
```

## 3. Basic Usage

Here is a quick example to verify that everything is working correctly.

Create a new file named `app.py` and add the following code:

```python
import calculator

# Initialize the calculator
calc = calculator.operations()

# Run a quick test function
result = calc.add(2, 3)
print(result)
```

Run your script from the terminal:

```bash
python app.py
```

**Expected Output:**

```text
Hello, World! Welcome to my-project.
```

## 4. Next Steps

Now that you have the basic application running, check out these resources to go deeper:

* Review the full [API Reference](../api/reference.md) for detailed class definitions.
* Check out the **Configuration Guide** to customize your setup.
