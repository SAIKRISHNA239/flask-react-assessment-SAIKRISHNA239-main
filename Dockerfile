FROM ubuntu:24.04
ARG DEBIAN_FRONTEND=noninteractive

# 1. Set locale
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

WORKDIR /app

# 2. Install system dependencies
# Update: Changed 'libasound2' to 'libasound2t64' for Ubuntu 24.04 compatibility
RUN apt-get update -y && \
  apt-get install -y build-essential git curl jq \
  python3-pip python3-venv python3-dev \
  libnotify-dev libnss3 libxss1 libasound2t64 libxtst6 xauth xvfb

# 3. Install pipenv
# We use --break-system-packages because we are inside a container, so it's safe.
RUN pip3 install pipenv --break-system-packages

# 4. Install Node.js 22
RUN curl -sL https://deb.nodesource.com/setup_22.x -o nodesource_setup.sh && \
  bash nodesource_setup.sh && \
  apt-get install -y nodejs && \
  node --version && npm --version

# 5. Setup Backend Dependencies
COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock

# Install Python dependencies
# We explicitly point to /usr/bin/python3 which is Python 3.12
RUN pipenv install --dev --python /usr/bin/python3

# 6. Setup Frontend Dependencies
RUN cp -a /app/. /.project/
COPY package.json /.project/package.json
COPY package-lock.json /.project/package-lock.json

RUN cd /.project && npm ci
RUN mkdir -p /opt/app && cp -a /.project/. /opt/app/

WORKDIR /opt/app

# Final install to ensure sync in the working directory
RUN npm ci
RUN pipenv install --dev --python /usr/bin/python3

COPY . /opt/app

# 7. Build and Start
ARG APP_ENV
RUN npm run build

CMD [ "npm", "start" ]