import torch
from fastapi import FastAPI, File, UploadFile, Depends
from pydantic import BaseModel 
from PIL import Image
import io
from torchvision.models import ResNet
from torchvision.transforms import v2 as transforms
from app.model import load_model, load_transforms

class Result(BaseModel):
    category: str # The predicted category of the input image (predicted label)
    confidence: float # The confidence score of the prediction, between 0 and 1 (a probability)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Message": """Welcome to the Image Classification API! To get a prediction for an image, send a POST request to the /predict endpoint with the image data."""}

@app.post('/predict', response_model=Result)
async def predict(
    input_image: UploadFile = File(...),
    model: ResNet = Depends(load_model),
    transforms: transforms.Compose = Depends(load_transforms)
    ) -> Result:
    
    image = Image.open(io.BytesIO(await input_image.read())).convert('RGB')
    
    print(f'the image mode should be now RGB {image.mode}')
    
    image = transforms(image).reshape(1, 3, 224, 224) # .unsqueeze(0) also works to add a batch dimension
    
    model.eval()
    
    # We need this to return string labels instead of numeric class indices in the API response.
    categories = ['fresh_apple', 'fresh_banana', 'fresh_orange', 
                'rotten_apple', 'rotten_banana', 'rotten_orange'] # This should match the order of classes used during training

    with torch.inference_mode():
        logits = model(image)
        probs = torch.nn.functional.softmax(logits, dim=1)
        confidence, predicted_class_idx = torch.max(probs, dim=1)
        predicted_category = categories[predicted_class_idx.item()]
    
    result = Result(category=predicted_category, 
                    confidence=confidence.item())
    return result

