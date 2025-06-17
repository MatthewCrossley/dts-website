FROM debian:12
RUN apt-get update && apt-get install -y \
    nodejs \
    npm

COPY . /frontend/
RUN chmod -R 755 /frontend/

WORKDIR /frontend
RUN npm cache clean --force
RUN npm install && npm run build

EXPOSE 3000
# EXPOSE 8000

ENTRYPOINT ["npm"]
CMD ["run", "start"]
