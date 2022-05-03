from random import sample
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, make_response
from grpc import StatusCode
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
import model
import audio_tools as at
import time


app = Flask(__name__)

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads/')
ALLOWED_EXTENSIONS = {'wav', 'mp3'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            timestr = time.strftime("%Y%m%d-%H%M%S")
            ext = ".wav"
            filename = f"{timestr}{ext}"
            file.save(join(app.config['UPLOAD_FOLDER'], filename))
            data = {'message': 'Upload successful', 'filename': filename, 'code': 'SUCCESS'}
            return make_response(jsonify(data), 201)
    return "error"

@app.route('/result', methods=['GET'])
def result():
    filename = request.args.get('n')
    wav_data = at.process_audio(filename)
    waveform = wav_data / model.tf.int16.max
    scores, embeddings, spectrogram = model.model(waveform)
    scores_np = scores.numpy()
    spectrogram_np = spectrogram.numpy()
    infered_class = model.class_names[scores_np.mean(axis=0).argmax()]
    return infered_class

if __name__ == '__main__':
    app.run(host='0.0.0.0')