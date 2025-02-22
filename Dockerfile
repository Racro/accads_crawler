# Use the latest Ubuntu image
FROM ubuntu:latest
# FROM node:18.20.4-alpine3.20

# Use the latest Ubuntu image
FROM ubuntu:latest

RUN apt-get update

# Install necessary packages
RUN apt-get install -y chromium-browser libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libx11-xcb1 libxcomposite1 libxcursor1 libxdamage1 libasound2t64 libxi6 libxtst6 libnss3 libxss1 libxrandr2 libpangocairo-1.0-0 libgtk-3-0 libgbm1 xdg-utils fonts-liberation libappindicator3-1 lsb-release wget git xvfb nodejs npm vim unzip

# Install necessary packages
RUN apt-get install -y x11-xkb-utils xkb-data

# Fix ownership of /tmp/.X11-unix
RUN mkdir -p /tmp/.X11-unix && chown root:root /tmp/.X11-unix && chmod 1777 /tmp/.X11-unix

# RUN chown root:root /tmp/.X11-unix && sudo chmod 1777 /tmp/.X11-unix

# Install the chrome 97
# RUN wget -q 'https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F978038%2Fchrome-linux.zip?generation=1646544045015587&alt=media' -O /tmp/chrome_97.zip && unzip /tmp/chrome_97.zip -d /tmp/chrome_temp && mv /tmp/chrome_temp/chrome-linux /tmp/chrome_97
# && mv /tmp/chrome-linux /tmp/chrome_97

# Install NPM version
RUN npm install -g npm@9.6.5

# Create a non-root user to run Chromium
RUN useradd -m chromiumuser
USER chromiumuser
WORKDIR /home/chromiumuser

COPY docker_in.py /home/chromiumuser/docker_in.py

# Install the git repo
RUN git clone https://github.com/Racro/accads_crawler.git

RUN wget -q 'https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F978038%2Fchrome-linux.zip?generation=1646544045015587&alt=media' -O /home/chromiumuser/accads_crawler/chrome_97.zip && unzip /home/chromiumuser/accads_crawler/chrome_97.zip -d /home/chromiumuser/accads_crawler/

# ./saved_session /home/chromiumuser/accads_crawler/saved_session

# Install puppeteer
# RUN cd accads_crawler && npm i --verbose

# Set the entrypoint to start Chromium
# ENTRYPOINT ["npm", "run", "crawl", "--", "-u", "", "-o", "./control", "-v", "-f", "-d", "ads", "--reporters", "cli,file", "-l", "./control/", "--autoconsent-action", "optIn"]
