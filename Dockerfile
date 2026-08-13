# ១. ចាប់ផ្តើមពី base image ដែលមាន Python ស្រាប់
FROM python:3.12-slim

# ២. កំណត់ folder ធ្វើការក្នុង container
WORKDIR /app

# ៣. Copy requirements មុន (សម្រាប់ caching!)
COPY requirements.txt .

# ៤. ដំឡើង dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ៥. Copy code ចូល
COPY app.py .

# ៦. ប្រាប់ថា app ស្តាប់ port 5000
EXPOSE 5000

# ៧. Command ដែល run ពេល container ចាប់ផ្តើម
CMD ["python", "app.py"]
