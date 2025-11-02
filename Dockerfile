# ---- Base image ----
FROM python:3.11-slim

# ---- Working directory ----
WORKDIR /app

# ---- Copy source code ----
COPY . .

# ---- Install dependencies ----
RUN pip install --no-cache-dir -r requirements.txt

# ---- Expose port ----
EXPOSE 8000

# ---- Environment (Flask run inside container) ----
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# ---- Command to run ----
CMD ["python", "app.py"]
