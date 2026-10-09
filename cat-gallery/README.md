# Cat Gallery

Cat Gallery is a Spring Boot application for publishing cat pictures and comments. Users can register, sign in, search the gallery, update profiles, and manage comments.

## Run locally

```bash
./gradlew bootRun
```

Open `http://localhost:8080` after the application starts.

## Build a container

```bash
docker build -t cat-gallery .
docker run --rm -p 8080:8080 cat-gallery
```

The application uses an in-memory H2 database populated by `DataInitializer` at startup.
