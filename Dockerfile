FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY app/ /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

#
EXPOSE 5000

# Run the app
CMD ["flask", "run", "--host=0.0.0.0"]
