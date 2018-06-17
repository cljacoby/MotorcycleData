# Motorcycle Data
A web scraper to collect a dataset of motorcycle models. The scraper writes its results as a JSON file, named by default motorcycles.json. The recorded attributes are "year", "make", "model", and "trim". Trim is optional and will be absent if that motorcycle entry lacks varying trim levels.

The project requires python3 and virtualenv. Virtualenv can be installed via:

`pip install virtualenv`

The project also uses selenium, which can be obtained via:

`pip install selenium`

Alternatively, you can also use either run.sh or run.bat to install selenium to the virtual python environment before running the main script.