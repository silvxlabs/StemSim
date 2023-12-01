# StemSim

## Running in Docker

First, build the image with

```bash
docker build -t stemsim .
```

Then run the container with

```bash
docker run --rm -p 80:80 stemsim
```

The API endpoint should be available at `http://localhost:80`.