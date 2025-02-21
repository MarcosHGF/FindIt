# Object Finder

Object Finder is an AI-powered application that helps locate specific objects in images. Simply provide an image and describe the object you're looking for (e.g., "Where is my wallet?"). The app will analyze the image, detect objects, and provide a natural language response describing the object's location and nearby items.

## 🚀 Features
- **Object Detection**: Uses YOLO to detect objects in images.
- **Natural Language Processing (NLP)**: Understands user queries and maps them to detected objects.
- **Proximity Detection**: Identifies nearby objects and provides contextual descriptions (e.g., "Your wallet is near the table").
- **Bounding Box Visualization**: Displays annotated images with bounding boxes around detected objects.
- **Cross-Platform Compatibility**: Works on both Android and iOS devices.

## 🛠 Technologies Used

### Backend
- **Python**: Core programming language for the backend.
- **Flask**: Lightweight web framework for handling API requests.
- **YOLO (v5/v7/v8)**: State-of-the-art object detection model.
- **spaCy**: NLP library for understanding user input.
- **Hugging Face Transformers**: Generates natural language responses.
- **OpenCV**: Processes and annotates images with bounding boxes.

### Frontend
- **React Native**: Mobile-friendly frontend framework.
- **Expo**: Simplifies React Native development and deployment.
- **Axios**: Handles HTTP requests to the backend.
- **ImagePicker**: Allows users to select images from their device.

### Deployment
- **Ngrok**: Exposes the Flask backend locally during development.

## 📸 How It Works
1. **Upload an Image**: Select an image from your device.
2. **Ask a Question**: Type a query like "Where is my wallet?" or "Find the teddy bear."
3. **Get Results**:
   - The app detects objects in the image.
   - It identifies the requested object and describes its location.
   - Nearby objects are mentioned for context.
4. **View Annotated Image**: See the image with bounding boxes around detected objects.

## 📋 Example Use Case
### Input
- **Image**: A photo of a room containing a book, a table, and a bottle.
- **Query**: "Where is my book?"

### Output
- **Response**: "Your book is in the center, near the table and the bottle."
- **Annotated Image**: The image will be displayed with bounding boxes around the wallet, table, and bottle.

## 🛠 How to Use

### Prerequisites
- Python 3.x installed on your system.
- Node.js and npm/yarn installed for the frontend.
- A mobile device or emulator for testing the React Native app.

### Backend Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/object-finder.git
   cd object-finder/backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask server:
   ```bash
   python app.py
   ```
   The backend will be available at `http://localhost:5000`.

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the app:
   ```bash
   npx expo start
   ```
4. Scan the QR code with the Expo Go app on your mobile device or use an emulator.

### Testing Locally
1. Use Ngrok to expose the backend to the frontend:
   ```bash
   ngrok http 5000
   ```
2. Update the frontend API endpoint in `App.js` with the Ngrok URL.

## 📂 Project Structure
```
object-finder/
├── backend/
│   ├── app.py                # Main Flask application
│   ├── requirements.txt      # Python dependencies
│   ├── object_detection.py   # Object detection logic
│   ├── nlp_processing.py     # NLP-related functions
│   ├── response_generator.py # Response generation logic
│   ├── utils.py              # Utility functions
│   └── known_classes.py      # List of known object classes
├── frontend/
│   ├── App.js                # React Native frontend
│   ├── package.json          # Frontend dependencies
│   └── assets/               # Images and other assets
└── README.md                 # This file
```

## 🔧 Customization

### Adding New Classes
If you want to detect objects not included in the default YOLO models:
1. Train a custom YOLO model with your dataset.
2. Replace the pre-trained model in the backend with your custom model.

### Improving NLP
1. Add more synonyms or mappings in the `word_mapping` dictionary.
2. Fine-tune spaCy or CLIP for better text understanding.

---
This README has been optimized for clarity and accuracy, removing errors and improving structure to facilitate project implementation. 🚀

