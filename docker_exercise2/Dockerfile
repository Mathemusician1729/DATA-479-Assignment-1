# Step 1: Base image
FROM python:3.9-slim

# Step 2: Set working dir
WORKDIR /app

# Step 3: Copy dependencies first (Better caching!)
COPY requirements.txt .

# Step 4: Install dependencies
RUN pip install -r requirements.txt

# Step 5: Copy the rest of the code
COPY . .

# Step 6: Command to run
CMD ["python3", "app.py"]