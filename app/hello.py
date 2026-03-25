from loadotenv import load_env 
import os

assert 'WANDB_API_KEY' in os.environ, "WANDB_API_KEY not found in environment variables"

