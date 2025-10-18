# kahoot-db/Dockerfile
FROM postgres:15

# Set environment variables (can also be done in docker-compose)
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=kahootdb

# Optionally copy initialization SQL scripts
# (they run automatically when the container starts)
# COPY init.sql /docker-entrypoint-initdb.d/
