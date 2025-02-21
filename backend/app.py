from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from PIL import Image
import cv2
import numpy as np
import base64
import spacy
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import warnings

# Ignorar avisos desnecessários
warnings.filterwarnings("ignore", category=FutureWarning)

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

# Carregar modelo NLP (spaCy) para inglês
nlp = spacy.load("en_core_web_sm")

# Carregar modelo YOLO para detecção de objetos
model_yolo = torch.hub.load('ultralytics/yolov5', 'yolov5l', pretrained=True)
model_yolo.conf = 0.1  # Reduzir o limiar de confiança
model_yolo.iou = 0.3   # Reduzir o IOU threshold

# Carregar modelo de geração de texto (Hugging Face)
tokenizer = AutoTokenizer.from_pretrained('gpt2')
model = AutoModelForCausalLM.from_pretrained('gpt2')

# Definir pad_token_id explicitamente
tokenizer.pad_token = tokenizer.eos_token

generator = pipeline('text-generation', model=model, tokenizer=tokenizer, truncation=True)

@app.route('/find_object', methods=['POST'])
def find_object():
    try:
        # Receber imagem e mensagem
        if 'image' not in request.files or 'message' not in request.form:
            return jsonify({"error": "Image or message not provided"}), 400

        image_file = request.files['image']
        text_message = request.form['message']

        print("Image file received:", image_file.filename)
        print("Message received:", text_message)

        # Validar imagem
        if image_file.filename == '':
            return jsonify({"error": "Invalid image"}), 400

        # Processar a mensagem para extrair o objeto
        object_name = extract_object_from_message(text_message)
        if not object_name:
            return jsonify({"error": "Could not extract the object from the message"}), 400

        # Processar a imagem para detectar objetos
        detected_objects, annotated_image_base64 = detect_objects_in_image(image_file)

        # Encontrar o objeto mencionado na imagem
        response = generate_response_with_context(object_name, detected_objects)

        return jsonify({
            "response": response,
            "detected_objects": detected_objects,  # Incluir lista de objetos detectados
            "annotated_image": annotated_image_base64  # Incluir imagem com bounding boxes
        })

    except Exception as e:
        print("Backend error:", str(e))
        return jsonify({"error": "An error occurred while processing your request", "details": str(e)}), 500

# Função para extrair o objeto da mensagem
def extract_object_from_message(message):
    doc = nlp(message)
    for token in doc:
        if token.pos_ == "NOUN":  # Procurar substantivos
            return token.text
    return None

# Função para detectar objetos na imagem e desenhar bounding boxes
def detect_objects_in_image(image_file):
    try:
        # Ler a imagem
        image = Image.open(image_file)
        image.verify()  # Verifica se é uma imagem válida
        image = Image.open(image_file)  # Reabrir para processamento
        image_cv2 = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)  # Converter para formato OpenCV

        results = model_yolo(image_cv2)
        objects = []
        for obj in results.xyxy[0]:
            label = model_yolo.names[int(obj[-1])]
            confidence = float(obj[4])  # Confiança da detecção
            x_min, y_min, x_max, y_max = map(int, obj[:4])  # Coordenadas da caixa delimitadora

            # Desenhar bounding box
            cv2.rectangle(image_cv2, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            cv2.putText(image_cv2, f"{label} {confidence:.2f}", (x_min, y_min - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            position = {
                "x_center": (x_min + x_max) // 2,
                "y_center": (y_min + y_max) // 2,
                "width": x_max - x_min,
                "height": y_max - y_min
            }
            objects.append({"name": label, "confidence": confidence, "position": position})

        # Calcular distâncias entre objetos
        for i, obj1 in enumerate(objects):
            obj1["nearby"] = []
            for j, obj2 in enumerate(objects):
                if i != j:  # Não comparar o objeto consigo mesmo
                    distance = calculate_distance(obj1, obj2)
                    if distance < 500:  # Limite arbitrário para "próximo"
                        obj1["nearby"].append(obj2["name"])

        # Converter a imagem anotada para Base64
        _, buffer = cv2.imencode('.jpg', image_cv2)
        annotated_image_base64 = base64.b64encode(buffer).decode('utf-8')

        return objects, annotated_image_base64
    except Exception as e:
        print("Error processing image:", str(e))
        return {"error": "Error processing image", "details": str(e)}, None

# Função para calcular a distância entre dois objetos
def calculate_distance(obj1, obj2):
    x1, y1 = obj1["position"]["x_center"], obj1["position"]["y_center"]
    x2, y2 = obj2["position"]["x_center"], obj2["position"]["y_center"]
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

# Função para gerar uma resposta natural com contexto
def generate_response_with_context(object_name, detected_objects):
    target_object = None
    nearby_objects = []

    # Encontrar o objeto mencionado
    for obj in detected_objects:
        if obj["name"] == object_name:
            target_object = obj
            break

    if not target_object:
        return f"I couldn't find your {object_name} in the image."

    # Encontrar objetos próximos
    nearby_objects = target_object.get("nearby", [])

    # Inferir região
    region = infer_region(target_object["position"])

    # Gerar resposta
    if nearby_objects:
        nearby_text = ", ".join(nearby_objects)
        return f"Your {object_name} is in the {region}, near the {nearby_text}."
    else:
        return f"Your {object_name} is in the {region}."

# Função para inferir a região do objeto
def infer_region(position):
    x_center, y_center = position["x_center"], position["y_center"]

    if x_center < 300 and y_center < 300:
        return "top-left corner"
    elif x_center > 300 and y_center < 300:
        return "top-right corner"
    elif x_center < 300 and y_center > 300:
        return "bottom-left corner"
    elif x_center > 300 and y_center > 300:
        return "bottom-right corner"
    else:
        return "center"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)  # Rodar em todas as interfaces