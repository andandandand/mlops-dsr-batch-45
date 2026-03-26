# Set Python version for the base image
FROM python:3.12-slim 


# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the working directory
COPY ./requirements.txt /code/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
	pip install --no-cache-dir -r /code/requirements.txt

# Copy the entire project into the working directory
COPY ./app /code/app

ENV WANDB_ORG=""
ENV WANDB_PROJECT=""
ENV WANDB_MODEL_NAME=""
ENV WANDB_MODEL_VERSION=""
ENV WANDB_API_KEY=""

EXPOSE 8080

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]