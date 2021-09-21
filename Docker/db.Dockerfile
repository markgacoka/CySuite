FROM postgres:10-alpine
COPY init.sql /docker-entrypoint-initdb.d/