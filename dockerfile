FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /code/

RUN python tienda/manage.py collectstatic --noinput
RUN python tienda/manage.py migrate --noinput


# Expone el puerto en el que correrá la aplicación
EXPOSE 8000

# Run the Django development server
CMD ["python", "tienda/manage.py", "runserver", "0.0.0.0:8000"]