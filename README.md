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
