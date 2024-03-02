# Usa una imagen base de Python
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de la aplicación al contenedor
COPY . .

RUN pip install --no-cache-dir --upgrade pip setuptools

# Instala las dependencias de la aplicación
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto en el que tu aplicación Flask se ejecuta dentro del contenedor
EXPOSE 5000

# Define el comando para ejecutar tu aplicación cuando el contenedor se inicie
CMD ["python3", "pacman.py"]
