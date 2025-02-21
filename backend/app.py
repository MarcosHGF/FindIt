from flask import Flask, request, jsonify
from flask_cors import CORS
from object_detection import detect_objects_in_image
from nlp_processing import extract_object_from_message
from response_generator import generate_response_with_context

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/find_object', methods=['POST'])
def find_object():
    try:
        # Receive image and message
        if 'image' not in request.files or 'message' not in request.form:
            return jsonify({"error": "Image or message not provided"}), 400

        image_file = request.files['image']
        text_message = request.form['message']

        print("Image file received:", image_file.filename)
        print("Message received:", text_message)

        # Validate image
        if image_file.filename == '':
            return jsonify({"error": "Invalid image"}), 400

        # Process the message to extract the object
        object_name = extract_object_from_message(text_message)
        if not object_name:
            return jsonify({"error": "Could not extract the object from the message"}), 400

        # Process the image to detect objects
        detected_objects, annotated_image_base64 = detect_objects_in_image(image_file)

        # Generate a natural language response
        response = generate_response_with_context(object_name, detected_objects)

        return jsonify({
            "response": response,
            "detected_objects": detected_objects,  # Include list of detected objects
            "annotated_image": annotated_image_base64  # Include annotated image
        })

    except Exception as e:
        print("Backend error:", str(e))
        return jsonify({"error": "An error occurred while processing your request", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)  # Run on all interfaces