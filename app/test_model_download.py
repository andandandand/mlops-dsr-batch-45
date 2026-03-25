from loadotenv import load_env 
import os
load_env() # this loads the variables in the .env file into the environment variables
assert 'WANDB_API_KEY' in os.environ, "WANDB_API_KEY not found in environment variables"
import wandb 

artifact_path = "jaguars/mlops_dsr_batch_45/resnet18:v1"

MODELS_DIR = "models"
MODEL_FILENAME = 'best_model.pth'

# this will create the models directory if it doesn't exist, and do nothing if it already exists
os.makedirs(MODELS_DIR, exist_ok=True)

wandb.login(key=os.getenv('WANDB_API_KEY'))    
api = wandb.Api()

artifact = api.artifact(artifact_path, type='model')
artifact.download(root=MODELS_DIR)


