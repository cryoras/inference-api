from flask import Flask, jsonify ,request
from src.utils import cleaningText, caseFold, tokenizeText, filteringText, toSentence,tfid,download_image,clean_old_files,preprocess_image
from tensorflow.keras.models import load_model # type: ignore
import joblib
import time
import threading
from datetime import datetime
from urllib.parse import urlparse


v1_text_model = joblib.load('./src/v1_text.joblib')
app = Flask(__name__)

v1_image_model = load_model('./src/v1_model.keras')

cleaner_thread = threading.Thread(target=clean_old_files, daemon=True)
cleaner_thread.start()

@app.route('/v1_text', methods=['POST'])
def v1_text():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
        
    if "predict" not in data:
        return jsonify({"error": "Missing 'predict' field"}), 400

    x_predict = data["predict"]
    if not isinstance(x_predict, str):
        return jsonify({"error": "Input harus berupa string"}), 400
    
    try:
        x_clean = cleaningText(x_predict)
        x_case = caseFold(x_clean)
        x_clean = tokenizeText(x_case)
        x_filter = filteringText(x_clean)
        x_sentence = toSentence(x_filter)
        x_tfid = tfid(x_sentence)

        pred = v1_text_model.predict(x_tfid)
        valid = pred[0] == 1
        return jsonify({"predict": str(valid)}), 200  # OK

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500  # Internal Server Error


@app.route('/v1_image', methods=['POST'])
def v1_image():
    data = request.get_json()
    image_link:str = data["image-link"]
    if not isinstance(image_link, str):
        return jsonify({"error": "Input harus berupa string"}), 400
    
    if not urlparse(image_link).scheme in ['http', 'https']:
        return jsonify({"error": "Invalid URL format"}), 400
    
    try:
        filename = f"image_{int(time.time())}.jpg"
        filepath,status = download_image(image_link, filename)
        img = preprocess_image(filepath)
        pred = v1_image_model.predict(img)
        img_pred = 1 if pred[0][0] > 0.5 else 0
        print("Kelas yang diprediksi:", pred[0][0])
        if filepath:
            return jsonify({"message": "Image downloaded", "filepath": filepath,"valid":img_pred})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500  # Internal Server Error


if __name__ == '__main__':
    app.run(debug=True)

