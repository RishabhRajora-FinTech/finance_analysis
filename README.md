source venv/bin/activate

####
Run the following command in the terminal to generate a requirements.txt file based on the libraries installed in your environment:

```
pip freeze > requirements.txt

```

This will create a requirements.txt file with all the installed Python packages and their versions. You can manually edit the file to include only the libraries used in your code (streamlit, pandas, yfinance, and matplotlib).



###

To set up a lock file or TOML file for Python library versioning, you can use tools like pipenv or poetry. Here's how to do it with each tool:

Using pipenv:
Install pipenv:
pip install pipenv
Create a Pipfile and Pipfile.lock:
pipenv install
Add your dependencies:
pipenv install streamlit==1.25.0 pandas==1.5.3 yfinance==0.2.30 matplotlib==3.7.2
This will generate a Pipfile and Pipfile.lock for version management.