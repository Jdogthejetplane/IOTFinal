
FROM nginx:alpine

# Remove default nginx index
RUN rm -rf /usr/share/nginx/html/*

# Copy your dashboard HTML
COPY index.html /usr/share/nginx/html/index.html

EXPOSE 80

# use default nginx entrypoint/cmd
