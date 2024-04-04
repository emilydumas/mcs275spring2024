# MCS 275 Spring 2024
"Flask demo of dynamically generated matplotlib plots"

import flask
import numpy as np
import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plt
import PIL.Image
import io
import random
import threading

# This object ensures only one request can be
# using matplotlib at a time.  That's important
# because matplotlib doesn't let you construct
# multiple figures simultaneously.
matplotlib_lock = threading.Lock()

# Create Flask (application) object
app = flask.Flask(__name__)

# Static HTML page that contains reference to a SVG
# image that is actually a dynamically generated plot
#-------------------------------------------------
# DON'T USE STRINGS TO SERVE HTML, USE TEMPLATES!
#-------------------------------------------------
# The only reason we use a string is so that
# this demo is contained in a single file
@app.route("/")
def front():
    return """<!doctype html>
<html>
    <head>
    <title>Random dynamic plots</title>
    <style>
    body { max-width: 45rem; margin: auto; }
    </style>
    </head>
    <body>
    <h1>Random line plot</h1>
    <p>This page contains random plots.  Every time you reload the page,
    new ones are generated.  No files are stored on disk.</p>
    <p>This one is a vector image (SVG):</p>
    <img src="/randomplot.svg">
    <p>And this one is a PNG image.</p>
    <img src="/randomplot.png">
    </body>
    </html>
"""


@app.route("/randomplot.<format>")
def random_plot(format):
    """
    Route that looks like the name of an image file but is
    actually a dynamically generated image.  The format can
    be svg or png, and it serves an image of that type.
    """

    # Ensure we have exclusive access to matplotlib
    # in this block.
    with matplotlib_lock:
        # Make random data
        x = np.linspace(0,1,20)
        y = np.random.random(x.shape)
        plt.figure(figsize=(4,3),dpi=90)
        plt.plot(x,y)
        plt.title("Random plot #{}".format(random.randint(10000,99999)))

        # Matplotlib can save a figure to a file, but not to memory
        # But Python has a class (BytesIO) that lets you create a
        # fake file object where the data stays in memory.
        fake_output_file = io.BytesIO()

        # Write the image data to "file" (really memory)
        plt.savefig(fake_output_file,format=format)
        fake_output_file.seek(0)  # Put file pointer back at start so we can read it back

        # Ask Flask to return the contents of our "file"
        # (The "mimetype" tells the receiving browser what sort of data
        #  is being sent, and is essential so that the file type is 
        #  recognized.)
        mt = { "png":"image/png", "svg":"image/svg+xml" }

        return flask.send_file(fake_output_file, mimetype=mt[format], max_age=0)
        # Omit max_age on the last line if it's OK for the image to be
        # cached (i.e. stored by the browser for use the next time the
        # page is loaded).


app.run()
