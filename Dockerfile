FROM python:3.12-slim

WORKDIR /code

# Copy all project files
COPY . /code/

# Install Poetry
RUN pip install poetry

# Install dependencies without installing the current project
RUN poetry install --no-interaction --no-cache --no-root

# Set environment variables
ENV PYTHONPATH=/code

# Expose port
EXPOSE 80

# Run the application
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]