SCIWYRM -- render jupyter notebooks for scicat data
===================================================

For development
===============
installing (in a python 3.11+ environment):
```
pip install "uvicorn[standard]"
pip install -e .
```

running:

```
uvicorn sciwyrm.main:app --reload
```

access:

```
navigate browser to:
http://localhost:8000/docs
```

In order to test, you can submit the following POST request , once you have the service running locally:
```
curl \ 
  -H 'Content-Type: application/json' \
  -d '{ 
    "template_id" : "b32f6992-0355-4759-b780-ececd4957c23", 
    "parameters" : {
      "dataset_pids" : [ "dataset_pid_1" ,"dataset_pid_2" ],
      "file_server_host" : "this_file_server",
      "file_server_port" : 22, 
      "scicat_url" : "my.scicat.instance", 
      "scicat_token" : "my.scicat.token"
    }
  }' \
  -X POST \
  http://localhost:8000/notebook
```
as a one liner, ready to be run, it looks like:
```
curl -H 'Content-Type: application/json' -d '{ "template_id" : "b32f6992-0355-4759-b780-ececd4957c23", "parameters" : {"dataset_pids":["dataset_pid_1","dataset_pid_2"],"file_server_host": "this_file_server","file_server_port" : 22, "scicat_url":"my.scicat.instance", "scicat_token" : "my.scicat.token"}}' -X POST http://localhost:8000/notebook
```

This request should result in an populated instance of the template b32f6992-0355-4759-b780-ececd4957c23.ipynb included in the repository.

## Docker Image
A docker image is created by a dedicated workflow everytime there is a new release by merging a PR in the `release` branch.

In case a users or developer has the need to create locally a docker image and deploy the container, the following commands can be used, assuming that image name `sciwyrm` and the container name is `scijug`:

Docker image creation
```
docker build -f docker/Dockerfile . -t sciwyrm

```

Docker container instantiation
```
docker create --name scijug -p 8000:8000 sciwyrm
```

The Jupyter creation service will be available on http://localhost:8000

## Contribution
All contributors should create a branch dedicated brnach to develop their feature and [performing their work.
Once the code is in a ready, the contribution should be done through a PR to the main branch, where maintainers can review, provide feedback and approve it. 

## Releases
Release are managed by maintainers by creating PRs from the main branch to the release branch.
Merging a PR in release trigger a git workflow that creates a release in the repository and also the creation of a docker image with the version of the service released.

