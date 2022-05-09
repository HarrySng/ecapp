# ecapp
Flask App for Downloading Environment Canada Climate Data

## Installation

1. Download the code to your local desktop.
2. Make sure you have docker installed.
3. Run the following command to build the docker image.

```zsh
docker build --tag ecapp-docker .
```

4. Run the docker image with the following command.

```zsh
docker run -d -p 5000:5000 ecapp-docker
```

5. Check running containers with the following command.

```zsh
docker ps
```

6. Access the app in your browser at the following address: <http://127.0.0.1:5000/>

7. Stop the container with the following command.

```zsh
docker stop <container-name>
```
