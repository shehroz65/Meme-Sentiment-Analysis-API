from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import torch
import torchvision.transforms as transforms
from PIL import Image

app = FastAPI()

# Initialize Jinja2Templates with the directory containing your HTML files
templates = Jinja2Templates(directory="templates")

# Load the saved model
combined_model = torch.load("combined_model_weights.pth")
combined_model.eval()  # Set the model to evaluation mode

# Transformation pipeline for preprocessing
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.filename:
        return "Please upload a file!"
    image = Image.open(file.file).convert('RGB')
    image = transform(image).unsqueeze(0)
    with torch.no_grad():
        sentiment_output, humor_output = combined_model(image)
        _, sentiment_predicted = torch.max(sentiment_output, 1)
        _, humor_predicted = torch.max(humor_output, 1)
    
    sentiments = ["Positive", "Negative"]  # Replace with your classes if different
    humors = ["Funny", "Not Funny"]        # Replace with your classes if different
    sentiment = sentiments[sentiment_predicted.item()]
    humor = humors[humor_predicted.item()]
    
    return templates.TemplateResponse('result.html', {
        "request": Request, 
        "sentiment": sentiment, 
        "humor": humor
    })