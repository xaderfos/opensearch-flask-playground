# A playground for testing out an Opensearch backend

## Opensearch

Using opensearch with the aim to try it out on the AWS free tier.

We can throw documents at Opensearch and then perform searches on them.

```shell
# In one terminal run this 
docker run -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" opensearchproject/opensearch:latest
```

## Flask based API

A basic API example using python Flask.

```shell
# macOS/Linux
# You may need to run sudo apt-get install python3-venv first
python3 -m venv .venv

# Windows
# You can also use py -3 -m venv .venv
python -m venv .venv


# activate macOS, no clue about windows...
. .venv/bin/activate

pip install opensearch-py
pip install Flask

python api.py
```

## Next

- Some minor setup issues prevent me from being able to use docker-compose.
The next step is to write a compose file for running Opensearch and the API.