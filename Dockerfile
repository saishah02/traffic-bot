FROM python:3.11-slim

# Elak prompt interactive masa apt install
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install Chrome + deps
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg \
    libglib2.0-0 libnss3 libgconf-2-4 libxi6 libxcursor1 libxcomposite1 \
    libasound2 libatk1.0-0 libatk-bridge2.0-0 libxrandr2 libxss1 libxtst6 \
    fonts-liberation xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Tambah repo Google Chrome
RUN curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-linux.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot code
COPY . .

# Default command: run bot
CMD ["python", "screenshot_bot.py"]
