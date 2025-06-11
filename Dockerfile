# Gunakan base image Python
FROM python:3.10-slim

# Atur working directory di dalam container
WORKDIR /app

# Salin requirements dan install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file project ke dalam container
COPY . .

# Jalankan script prediksi (bisa disesuaikan)
CMD ["python", "predict.py"]