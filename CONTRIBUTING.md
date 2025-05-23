
# Contributing to vitap-vtop-client

Thank you for your interest in contributing to the `vitap-vtop-client` library! Your help is valuable in maintaining and enhancing this tool for interacting with the VIT-AP VTOP portal.

Web scraping projects like this are sensitive to changes in the target website. Contributions that help update the scraping logic, parsers, or fix issues caused by VTOP updates are especially appreciated.

## Code of Conduct

This project and everyone participating in it is governed by the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs
If you find a bug, please ensure the bug was not already reported by searching on GitHub under [Issues](https://github.com/Udhay-Adithya/vitap-vtop-client/issues).

If you're unable to find an open issue addressing the problem, [open a new one](https://github.com/Udhay-Adithya/vitap-vtop-client/issues/new). Be sure to include a **title and clear description**, as much relevant information as possible, and a **code sample or an executable test case** demonstrating the expected behavior that is not occurring.

Provide the following information:
- Your operating system name and version.
- Python version.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

### Suggesting Enhancements
If you have an idea for an enhancement, please first discuss the change you wish to make via a GitHub issue before making a change.

Provide the following information:
- A clear and descriptive title.
- A detailed description of the proposed enhancement.
- The motivation or use case for the enhancement.
- Any potential drawbacks or alternative solutions.

### Pull Requests
Pull Requests (PRs) are the primary way to contribute code to this project.

1.  **Fork the repository**: 

    Click the "Fork" button at the top right of the [repository page](https://github.com/Udhay-Adithyavitap-vtop-client).


2.  **Clone your fork**: 


```bash
git clone https://github.com/Udhay-Adithya/vitap-vtop-client.git
```


3.  **Create a new branch**: 


```bash
# For new-features
git checkout -b feature/your-feature-name
# For bug-fixes
bugfix/issue-number-description
```


4.  **Set up your development environment**: Follow the [Development Setup](#development-setup) instructions.
5.  **Make your changes**: Implement your feature or bug fix.
6.  **Follow Coding Guidelines**: Ensure your code adheres to the [Coding Guidelines](#coding-guidelines).
7.  **Add tests**: Write unit tests for your changes.
8.  **Commit your changes**: Use clear and descriptive [Commit Messages](#commit-messages).
9.  **Push to your fork**: `git push origin feature/your-feature-name`.
10. **Open a Pull Request**: Go to the original repository and open a PR from your forked branch to the `main` branch of the original repository.
    - Provide a clear title and description for your PR, linking to any relevant issues.
    - Ensure all automated checks (linters, tests) pass.

Project maintainers will review your PR and may request changes. Please be responsive to feedback.

## Development Setup
To set up the project for local development:

1.  **Clone the repository** (if you haven't already forked and cloned):
    ```bash
    git clone https://github.com/Udhay-Adithya/vitap-vtop-client.git
    cd vit_ap_vtop_api
    ```
2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    
## Coding Guidelines

### Python Style Guide
-   Follow [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/).
-   Use a linter like Flake8 or Pylint to check your code.
-   Keep functions and methods small and focused on a single task.
-   Add comments to explain complex logic or non-obvious code.
-   Use type hints where appropriate.

### Commit Messages
-   Use the present tense ("Add feature" not "Added feature").
-   Use the imperative mood ("Move cursor to..." not "Moves cursor to...").
-   Limit the first line to 72 characters or less.
-   Reference issues and PRs liberally.
-   Consider using [Conventional Commits](https://www.conventionalcommits.org/) for more structured commit messages, e.g.:
    -   `feat: add new endpoint for course registration`
    -   `fix: resolve issue with captcha parsing`
    -   `docs: update README with new setup instructions`
    -   `refactor: improve performance of attendance fetching`
    -   `test: add unit tests for profile parser`

## Testing
-   Write unit tests for new features and bug fixes.
-   Ensure all existing tests pass before submitting a PR.
-   Tests are typically located in a `tests/` directory (though not explicitly shown in the provided project structure, it's a best practice).
-   Use a testing framework like `pytest` or Python's built-in `unittest`.

## Documentation
-   Keep the [`README.md`](/README.md), [`DOCS.md`](/DOCS.md) and other documentation files up-to-date with your changes.
-   If you add new features or change existing ones, update the relevant sections of the documentation.
-   For API changes, ensure the endpoint descriptions, request/response formats, and examples are accurate.

## Community
Join the discussion! If you have questions or want to discuss ideas, feel free to open an issue or participate in existing discussions.

Thank you for contributing!