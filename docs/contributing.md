# Contributing

Contributions are welcome! Please follow these guidelines to keep development consistent and reliable.

## Development Workflow

1. Fork the repository and create a descriptive branch name (e.g., `feature/add-logarithms`).
2. Add your functions alongside explicit **type hints**.
3. Include **NumPy-style docstrings** for any new exposed endpoints.
4. Open a Pull Request pointing to the `main` branch.

## Code Style

We strictly follow basic styling guidelines. Ensure all mathematical edge cases (such as zero bounds or invalid operators) raise a contextual `ValueError`.
