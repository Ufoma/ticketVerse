import os
import uuid
from flask import Flask, request, send_file, jsonify
from werkzeug.utils import secure_filename
# from PIL import Image

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
TICKET_TEMPLATE = 'ticket_template.png'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_event_image():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify({'success': 'File uploaded successfully'}), 201
    return jsonify({'error': 'Invalid request'}), 400


def delete_event_image(image_id):
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_id)
    if os.path.exists(image_path):
        os.remove(image_path)
        return jsonify({'success': 'Image deleted successfully'}), 200
    return jsonify({'error': 'Image not found'}), 404


def generate_ticket(event_id, ticket_number):
    event_image_path = os.path.join(app.config['UPLOAD_FOLDER'], event_id)
    ticket_template = Image.open(TICKET_TEMPLATE)
    event_image = Image.open(event_image_path)
    ticket_template.paste(event_image, (100, 100))  # Adjust position
    ticket_text = f"Event ID: {event_id}\nTicket Number: {ticket_number}"
    ticket_template.text((100, 300), ticket_text,
                         fill=(0, 0, 0))  # Adjust position
    ticket_filename = f"{event_id}_{ticket_number}.png"
    ticket_template.save(ticket_filename)
    return send_file(ticket_filename, as_attachment=True)


@app.route('/upload', methods=['POST'])
def upload_image():
    return upload_event_image()


@app.route('/delete/<image_id>', methods=['DELETE'])
def delete_image(image_id):
    return delete_event_image(image_id)


@app.route('/generate_ticket/<event_id>/<ticket_number>', methods=['GET'])
def generate(event_id, ticket_number):
    return generate_ticket(event_id, ticket_number)


if __name__ == '__main__':
    app.run(debug=True)
