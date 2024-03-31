

FROM python:3.11
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libmagic1 \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*
# RUN apt-get install git build-essential gcc python3-dev musl-dev pkg-config -y

COPY Server/requirements.txt .
RUN pip install -r requirements.txt

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /Server
WORKDIR /Server
COPY ./Server /Server/

RUN python manage.py migrate
RUN python manage.py collectstatic --no-input


# Expose port for the Django development server
EXPOSE 8000

# Run Django server on container startup
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


