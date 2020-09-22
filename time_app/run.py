from flask import Flask
import datetime
from pytz import timezone
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/time')
def return_time():
    return str(datetime.datetime.now(timezone('US/Eastern')))


app.run(host='0.0.0.0',
        port=8080,
        debug=True)
