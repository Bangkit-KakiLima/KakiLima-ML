# Gunakan base image resmi Python
FROM python:3.9-slim

# Tetapkan direktori kerja di dalam container
WORKDIR /app

# Salin file requirements.txt untuk menginstal dependensi
COPY requirements.txt .

# Instal dependensi menggunakan pip
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file aplikasi ke dalam container
COPY . .

# Ekspos port 8080 (default untuk Google Cloud Run)
EXPOSE 8080

# Tetapkan variabel lingkungan untuk memastikan aplikasi FastAPI mendengarkan port yang benar
ENV PORT 8080

# Jalankan aplikasi menggunakan Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
