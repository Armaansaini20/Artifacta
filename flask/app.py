import os
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import requests
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure API keys
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
MESHY_API_KEY = os.getenv("MESHY_API_KEY")

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def get_gemini_response(input_text, image_data, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, image_data[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file:
        # Read the uploaded image file into bytes (no need to save to disk)
        image_data = uploaded_file.read()  # Read the file as bytes in memory

        # Prepare the image data in the required format
        image_parts = [
            {
                "mime_type": uploaded_file.mimetype,
                "data": image_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

def model(img_desc_response):
    payload = {
        "mode": "preview",
        "prompt": img_desc_response,
        "art_style": "realistic",
        "negative_prompt": "low quality, low resolution, low poly, ugly"
    }
    headers = {
        "Authorization": "Bearer msy_OQojQ61ITTBmpnjteMPszYy8ZY7XwBQEppXC"
    }

    # Post the request to create a new task
    response_taskid = requests.post(
        "https://api.meshy.ai/v2/text-to-3d",
        headers=headers,
        json=payload,
    )

    if response_taskid.status_code == 200:
        return {"error": "Failed to create Meshy task", "details": response_taskid.text}

    task_id = response_taskid.json().get('result')
    if not task_id:
        return {"error": "No task ID returned from Meshy"}

    print("task_id:", task_id)

    # Check the status of the task with a retry loop
    max_retries = 20
    retry_delay = 10  # seconds

    for attempt in range(max_retries):
        # Get the status of the task
        response = requests.get(
            f"https://api.meshy.ai/v2/text-to-3d/{task_id}",
            headers=headers,
        )

        if response.status_code != 200:
            return {"error": "Failed to get Meshy task status", "details": response.text}

        result = response.json()
        status = result.get('status')
        print(f"Attempt {attempt+1}/{max_retries} - Status: {status}")

        if status == "SUCCEEDED":
            model_urls = result.get('model_urls', {})
            glb_url = model_urls.get("glb")
            if glb_url:
                return {"glb_url": glb_url}
            else:
                return {"error": "GLB URL not found in Meshy response"}

        elif status == "FAILED":
            return {"error": "Meshy task failed", "details": result}

        else:
            print(f"Status: {status}. Progress: {result.get('progress')}%. Waiting...")
            time.sleep(retry_delay)

    return {"error": "Meshy task did not complete within the expected time."}

@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        input_prompt = """
        You are an expert in understanding invoices.
        You will receive input images as invoices & 
        you will have to answer questions based on the input image.
        """
        prompty = "check if the item in image is broken or not"
        img_desc = "describe the main image in fine details if the image has some faults or has broken parts. Fix the image into one and tell its details excluding the broken part with accurate color as described in image."

        # Check if the post request has the file part
        if 'image' not in request.files:
            return jsonify({"error": "No image part in the request"}), 400

        uploaded_file = request.files['image']
        if uploaded_file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Process the uploaded image
        image_data = input_image_setup(uploaded_file)

        # Generate responses using Gemini
        response_text = get_gemini_response(input_prompt, image_data, prompty)
        img_desc_response = get_gemini_response(input_prompt, image_data, img_desc)

        # Create Meshy task
        mesh_response = model(img_desc_response)

        return jsonify({
            "response": response_text,
            "response2": img_desc_response,
            "mesh_response": mesh_response
        })

    except Exception as e:
        app.logger.error(f"Error during task creation: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

#cd flask -> cd venv -> cd Scripts -> activate -> cd.. -> python app.py