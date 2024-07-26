# Use the latest Ubuntu image
FROM ubuntu:latest
# FROM node:18.20.4-alpine3.20

# Use the latest Ubuntu image
FROM ubuntu:latest

RUN apt-get update

# Install necessary packages
RUN apt-get install -y chromium-browser libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libx11-xcb1 libxcomposite1 libxcursor1 libxdamage1 libasound2t64 libxi6 libxtst6 libnss3 libxss1 libxrandr2 libpangocairo-1.0-0 libgtk-3-0 libgbm1 xdg-utils fonts-liberation libappindicator3-1 lsb-release wget git xvfb nodejs npm vim unzip

# Install the chrome 97
RUN wget -q 'https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F978038%2Fchrome-linux.zip?generation=1646544045015587&alt=media' -O /tmp/chrome_97.zip && unzip /tmp/chrome_97.zip -d /tmp/chrome_temp && mv /tmp/chrome_temp/chrome-linux /tmp/chrome_97
# && mv /tmp/chrome-linux /tmp/chrome_97

# Install NPM version
RUN npm install -g npm@9.6.5

# Create a non-root user to run Chromium
RUN useradd -m chromiumuser
USER chromiumuser
WORKDIR /home/chromiumuser

# Install the git repo
RUN git clone https://github.com/Racro/accads_crawler.git && cd accads_crawler

# Install puppeteer
RUN cd accads_crawler && npm i --verbose

# Set the entrypoint to start Chromium
# ENTRYPOINT ["npm", "run", "crawl", "--", "-u", "", "-o", "./control", "-v", "-f", "-d", "ads", "--reporters", "cli,file", "-l", "./control/", "--autoconsent-action", "optIn"]
