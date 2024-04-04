# MCS 275 Spring 2024
"Simple Flask demo that returns an image"

import flask
import numpy as np
import PIL.Image
import io

# Create Flask (application) object
app = flask.Flask(__name__)

# Static HTML page that contains reference to an image
# whose URL will call another route (below)
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
    <title>Random color static</title>
    <style>
    body { max-width: 45rem; margin: auto; }
    </style>
    </head>
    <body>
    <h1>Random color static</h1>
    <p>Here is your custom random color static image, generated just for you in response to this request.
    It is probably different from every image ever seen by humans, and will not be seen again.
    (After you reload or close the page, this image is lost.)</p>
    <img src="/random-color-static.png">
    </body>
    </html>
"""


@app.route("/random-color-static.png")
def color_static_image():
    """
    Route that looks like the name of an image file but is
    actually a dynamically generated image.  No file is 
    ever stored on disk; it's generated freshly every time
    it is requested.
    """
    # Make random data (matrix)
    data = (np.random.random((64, 64, 3)) * 255).astype("uint8")

    # Convert to random colorful small PIL image
    img = PIL.Image.fromarray(data)

    # Blow it up by a factor of 8
    img = img.resize((512, 512), resample=PIL.Image.NEAREST)

    # PIL can write PNG or JPEG to a file, but not to memory
    # But Python has a class (BytesIO) that lets you create a
    # fake file object where the data stays in memory.
    fake_output_file = io.BytesIO()

    # Have PIL write a PNG to that memory-backed fake file
    img.save(fake_output_file, "png")  # need to specify format in second arg
    fake_output_file.seek(0)  # Put file pointer back at start so we can read it back

    # Ask Flask to return the contents of our "file"
    # (The "mimetype" tells the receiving browser what sort of data
    #  is being sent, and is essential so that the file type is 
    #  recognized.)
    return flask.send_file(fake_output_file, mimetype="image/png", max_age=0)
    # Omit max_age on the last line if it's OK for the image to be
    # cached (i.e. stored by the browser for use the next time the
    # page is loaded).


app.run()
