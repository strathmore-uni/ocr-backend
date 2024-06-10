from flask import Flask, request, jsonify
import easyocr
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

reader = easyocr.Reader(['en'])

def convert_to_serializable(obj):
    if isinstance(obj, np.int32):
        return int(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (list, tuple)):
        return [convert_to_serializable(i) for i in obj]
    return obj

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    image = request.files['image']
    results = reader.readtext(image.read())
    serializable_results = [[convert_to_serializable(item) for item in result] for result in results]
    return jsonify(serializable_results)

if __name__ == '__main__':
    app.run(debug=True)
