from flask import Flask
from src import status

app = Flask(__name__)

# We will use the app decorator and create a route called slash counters.
# specify the variable in route <name>
# let Flask know that the only methods that is allowed to be called
# on this function is "POST".

COUNTERS = {}


@app.route('/counters/<name>', methods=['POST'])
def create_counter(name):
    """ Create a counter """
    app.logger.info(f'Request to create counter {name}')
    global COUNTERS
    if name in COUNTERS:
        return {'Message': f'Counter {name} already exists'}, status.HTTP_409_CONFLICT
    COUNTERS[name] = 0
    return {name: COUNTERS[name]}, status.HTTP_201_CREATED


@app.route('/counters/<name>', methods=['PUT'])
def update_counter(name):
    """ Update a counter """
    app.logger.info(f'Request to update counter {name}')
    global COUNTERS
    if name not in COUNTERS:
        return {'Message': f'Counter {name} not found'}, status.HTTP_404_NOT_FOUND
    if name in COUNTERS:
        if COUNTERS[name] is None:
            return {name: COUNTERS[name]}, status.HTTP_204_NO_CONTENT
        COUNTERS[name] = COUNTERS[name] + 1
        return {name: COUNTERS[name]}, status.HTTP_200_OK


@app.route('/counters/<name>', methods=['GET'])
def read_counter(name):
    app.logger.info(f'Request to read counter {name}')
    global COUNTERS
    if name not in COUNTERS:
        return {'Message': f'Counter {name} not found'}, status.HTTP_404_NOT_FOUND
    if name in COUNTERS:
        return {name: COUNTERS[name]}, status.HTTP_200_OK
