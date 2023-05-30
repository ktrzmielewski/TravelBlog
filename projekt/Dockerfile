# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file
COPY requirements.txt /app/requirements.txt

# Install project dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the project code into the container
COPY . .

# Expose the port that Django runs on
EXPOSE 8000

# Set environment variables if necessary
# ENV DJANGO_SETTINGS_MODULE=projekt.settings

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]