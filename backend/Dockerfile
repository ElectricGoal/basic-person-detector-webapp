FROM python:3.10-slim

RUN apt-get update && apt-get install -y postgresql-client

# Set work directory
WORKDIR .

# Copy application code
COPY . .

RUN chmod +x entrypoint.sh

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir opencv-python-headless

# Create the temp uploads folder
RUN mkdir -p temp_uploads

EXPOSE 8000

# Use the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
# Run the application
CMD ["bash", "gunicorn.sh"]
