# Running the code

Within the project directory, build the image and start a new container from the image:

```sh
docker build -t quorum .

docker run --name quorum -p 8000:8000 -d quorum
```

or start an existing stopped container:

```sh
docker start quorum
```


http://localhost:8000

The sample data was already loaded. If needed:

```sh
docker exec -it quorum python manage.py load_samples
```

There is also and admin user created:

- user = admin
- password = quorum.us

http://localhost:8000/admin