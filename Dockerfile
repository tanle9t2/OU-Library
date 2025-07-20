FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt


COPY . .
COPY .env .env

#
EXPOSE 5000

# Run the app
CMD ["flask", "run", "--host=0.0.0.0"]
