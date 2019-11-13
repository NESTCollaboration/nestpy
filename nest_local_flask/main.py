import io
import logging 
import os
import collections
from flask import Response, Flask, send_file, request
from benchmark_plots import makeplots

#  TODO: 
# In IMAGE_OBJECTS, check version of nestpy?  Or generate file upon request?

IMAGE_OBJECTS = collections.defaultdict(io.BytesIO)

makeplots(IMAGE_OBJECTS)
app = Flask(__name__)

@app.route('/get_image')
def get_image():
    filename = request.args.get('interaction') + '_' + request.args.get('yieldtype') + '.png'                                            
    file_object = IMAGE_OBJECTS[filename]
    file_object.seek(0)

    return send_file(file_object,
                     mimetype='image/png')

@app.route('/')
def hello():
    message = "Welcome to your very first Flask app of nestpy! At the end of this URL Type in:"
    typecommand = " /get_image?interaction=<type of interaction>&yieldtype=<either LY (light yield) or QY (charge yield)"
    return(message + typecommand)

if __name__ == '__main__':
    app.run(port=8080, debug=True)