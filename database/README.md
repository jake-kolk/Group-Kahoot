# Installation

## Development

### On Windows
1. `py -3.13 -m venv .venv`
In the repository
2. `.venv/Scripts/activate`
3. `pip install -r requirements.txt`
4. `python main_rest_api.py`


### Mac/Linux
1. `python3.13 -m venv .venv`
In the repository
2. `source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `python3 main_rest_api.py`

## Docker
1. `docker build -t kahoot-client .`
2. `docker run --rm -p 80:80 kahoot-client`
You can change the first port number 80 to whatever port you want

## API Documentation and testing
In your browser, go to https://localhost:8000
