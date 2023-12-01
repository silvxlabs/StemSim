# StemSim

## Docker

First, build the image with

```bash
docker build -t stemsim .
```

Then run the container with

```bash
docker run --rm -p 80:80 stemsim
```

The API endpoints should be available at `http://localhost:80`.

## Example client

Run the Python demo in the `example` directory

```bash
python demo.py
```