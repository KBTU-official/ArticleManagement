# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies with pinned versions
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Ensure SpaCy model is downloaded
RUN python -m spacy download en_core_web_sm

# Expose the port that Django runs on
EXPOSE 8000

# Run migrations and start the server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
