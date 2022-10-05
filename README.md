Install dependencies locally using virtual environment
Run the commands in bash terminal:
    python -m venv .env (create folder for packages/dependencies)
    source .env/Scripts/activate (activate virtual environment)
    pip install [package-name]

    optionals:
    pip freeze > requirements.txt (creates txt for dependencies)
    pip install -r requirements.txt (if exists; will install the listed packages)
