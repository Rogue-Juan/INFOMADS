Install dependencies locally using virtual environment
Run the commands in bash (my friend prefers this terminal) terminal:
    python -m venv .env (create folder for packages/dependencies)
    source .env/Scripts/activate (activate virtual environment; it can now use the installed packages)
    pip install [package-name] (install a specific package onto this environment)

    Optionals:
    pip freeze > requirements.txt (creates txt for dependencies)
    pip install -r requirements.txt (if it exists, it will install the listed packages)
