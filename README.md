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

This request should result in the following notebook:
```
{"cells":[{"cell_type":"markdown","id":"803f7b636cfa4b4c","metadata":{},"source":["# Generic\n","<span style=\"font-size: smaller\">Notebook generated from template '<em>Generic</em>' version 1 (id: `b32f6992-0355-4759-b780-ececd4957c23`, time: <time>2025-02-18T09:08:07.355287+00:00</time>).</span>"]},{"cell_type":"markdown","id":"9e7442fc9ec68975","metadata":{},"source":["This notebook downloads selected datasets from SciCat and all files for those datasets."]},{"cell_type":"code","execution_count":null,"id":"923ba88e07905c7b","metadata":{},"outputs":[],"source":["import scitacean\n","from scitacean.transfer.sftp import SFTPFileTransfer"]},{"cell_type":"markdown","id":"d0336f3a7a2d37eb","metadata":{},"source":["Scicat configuration:"]},{"cell_type":"code","execution_count":null,"id":"91d1974c665d73f3","metadata":{},"outputs":[],"source":["scicat_url = \"my.scicat.instance\"\n","file_server_host = \"this_file_server\"\n","file_server_port = 22"]},{"cell_type":"markdown","id":"9bdf7ecbf3cd7df","metadata":{},"source":["Login token for SciCat. If it expires, replace it with a new one obtained from the SciCat web interface."]},{"cell_type":"code","execution_count":null,"id":"31c3a003da7913e9","metadata":{},"outputs":[],"source":["scicat_token = \"my.scicat.token\""]},{"cell_type":"markdown","id":"590b037151d5a71d","metadata":{},"source":["Select datasets to downloads:"]},{"cell_type":"code","execution_count":null,"id":"initial_id","metadata":{},"outputs":[],"source":["input_dataset_pids = [\n","    \"dataset_pid_1\",\n","    \"dataset_pid_2\",\n","]"]},{"cell_type":"markdown","id":"a3358b891c9c476d","metadata":{},"source":["Download files to this folder. You may change it freely."]},{"cell_type":"code","execution_count":null,"id":"8f1a34476bf70da7","metadata":{},"outputs":[],"source":["file_download_folder = \"./download\""]},{"cell_type":"code","execution_count":null,"id":"1d0f975884ac9e5b","metadata":{},"outputs":[],"source":["scicat_client = scitacean.Client.from_token(\n","    url=scicat_url,\n","    token=scicat_token,\n","    file_transfer=SFTPFileTransfer(\n","        host=file_server_host,\n","        port=file_server_port,\n","    )\n",")"]},{"cell_type":"code","execution_count":null,"id":"dc6f6c8b285dfb16","metadata":{},"outputs":[],"source":["datasets = [\n","    scicat_client.download_files(\n","        scicat_client.get_dataset(pid),\n","        target=file_download_folder,\n","    )\n","    for pid in input_dataset_pids\n","]"]}],"metadata":{"kernelspec":{"display_name":"Python 3 (ipykernel)","language":"python","name":"python3"},"language_info":{"codemirror_mode":{"name":"ipython","version":3},"file_extension":".py","mimetype":"text/x-python","name":"python","nbconvert_exporter":"python","pygments_lexer":"ipython3","version":"3.11.5"},"sciwyrm":{"template_id":"b32f6992-0355-4759-b780-ececd4957c23","template_submission_name":"generic","template_display_name":"Generic","template_version":"1","template_authors":[{"name":"Jan-Lukas Wynen","email":"jan-lukas.wynen@ess.eu"}],"template_rendered_at":"2025-02-18T09:08:07.374669+00:00","template_hash":"blake2b:2df9ee51d76dd478976b2daa2395475f85d8597096ec5fd6620f618457994b4c559bbddc8a7edec3037a48322eaf96471ef52b85b8ad1bdd15a09d02cc95b4ff"}},"nbformat":4,"nbformat_minor":5}
```

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

