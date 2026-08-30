# n8n Docker Custom Build Workaround (Hardened Image Issue)

This document details the workaround for customizing n8n Docker containers when upgrading to newer 2.x versions, where the official base image (`n8nio/n8n:latest`) has migrated to a **Docker Hardened Image** that strips the package manager (`apk`).

## The Problem
When upgrading n8n in a custom Dockerfile that attempts to install runtime dependencies (e.g., `ffmpeg`, `python3`, `edge-tts`, custom fonts) via:
```dockerfile
FROM n8nio/n8n:latest
USER root
RUN apk add --no-cache ffmpeg python3 ...
```
The build fails with `/bin/sh: apk: not found` because `apk` is completely stripped in modern production n8n images.

## The Solution: Multi-Stage Build with Standard Node Base
To bypass this restriction, use a multi-stage Docker build. We extract the compiled `n8n` source module from the official hardened repository and run it on top of a standard, functional `node:alpine` base image containing the package manager.

Note: n8n 2.x requires **Node >= 24**. Using `node:20-alpine` will trigger a startup block error demanding Node 24.

### Correct Dockerfile Structure
Write the following configuration in `/opt/n8n/Dockerfile`:

```dockerfile
# Stage 1: Pull official n8n as code source
FROM n8nio/n8n:latest AS n8n-source

# Stage 2: Build on top of official Node Alpine (which has apk)
FROM node:24-alpine

# Set environment
ENV NODE_ENV=production

# Install system dependencies (FFmpeg, Python, Fonts tools, etc.)
RUN apk add --no-cache \
    ffmpeg \
    mesa-va-gallium \
    libva-utils \
    ttf-dejavu \
    font-adobe-100dpi \
    wget \
    python3 \
    py3-pip \
    bash \
    su-exec \
    ca-certificates

# Install Edge TTS (with --break-system-packages flag for modern Python standards)
RUN pip3 install --break-system-packages edge-tts || pip3 install edge-tts

# Copy fonts (Anton, Montserrat-Bold)
# Note: Montserrat-Bold has been removed from the google/fonts default directory,
# so download it from the official master ttf directory instead.
RUN mkdir -p /usr/share/fonts/truetype/custom
RUN wget -qO /usr/share/fonts/truetype/custom/Anton-Regular.ttf https://github.com/google/fonts/raw/main/ofl/anton/Anton-Regular.ttf
RUN wget -qO /usr/share/fonts/truetype/custom/Montserrat-Bold.ttf https://github.com/googlefonts/montserrat/raw/master/fonts/ttf/Montserrat-Bold.ttf
RUN fc-cache -f

# Copy the n8n source code (ignores the hardened Node binary)
COPY --from=n8n-source /usr/local/lib/node_modules/n8n /usr/local/lib/node_modules/n8n
RUN ln -sf /usr/local/lib/node_modules/n8n/bin/n8n /usr/local/bin/n8n

# Copy security certificates & entrypoint script
COPY --from=n8n-source /docker-entrypoint.sh /docker-entrypoint.sh
COPY --from=n8n-source /etc/ssl /etc/ssl

# Setup folders and running permissions
RUN mkdir -p /data_shared && chown -R node:node /data_shared
RUN addgroup -g 44 host_video || true
RUN addgroup -g 109 host_render || true
RUN addgroup node host_video || true
RUN addgroup node host_render || true

USER node

ENTRYPOINT ["/docker-entrypoint.sh"]
```

## Upgrade and Re-deployment Steps
1. **Always backup** the n8n database:
   `cp /opt/n8n/n8n_data/database.sqlite /opt/n8n/n8n_data/database_backup_$(date +%F).sqlite`
2. **Rebuild the image**:
   `docker compose build`
3. **Recreate the containers**:
   `docker compose up -d`
4. **Verify version**:
   `docker exec n8n_app n8n --version`
