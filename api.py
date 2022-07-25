from flask import Flask
from opensearchpy import OpenSearch
from uuid import uuid4

host = 'localhost'
port = 9200
auth = ('admin', 'admin') # For testing only. Don't store credentials in code.
ca_certs_path = '/full/path/to/root-ca.pem' # Provide a CA bundle if you use intermediate CAs with your root CA.

index_name = 'python-test-index'

# Create the client with SSL/TLS enabled, but hostname verification disabled.
client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_compress = True, # enables gzip compression for request bodies
    http_auth = auth,
    # client_cert = client_cert_path,
    # client_key = client_key_path,
    use_ssl = True,
    verify_certs = False,
    ssl_assert_hostname = False,
    ssl_show_warn = False,
    # ca_certs = ca_certs_path
)

def init():
    if not client.indices.exists(index_name):
        # Create an index with non-default settings.
        try:        
            index_body = {
            'settings': {
                'index': {
                'number_of_shards': 4
                }
            }
            }

            response = client.indices.create(index_name, body=index_body)
            print('\nCreating index:')
            print(response)
        except:
            pass

def search_fn(term):
    # Search for the document.    
    query = {
    'size': 5,
    'query': {
        'multi_match': {
        'query': term,
        'fields': ['title^2', 'director', 'year']
        }
    }
    }

    response = client.search(
        body = query,
        index = index_name
    )
    print('\nSearch results:')
    print(response)

    return response

def add_document(document):    
    
    id = uuid4().int

    response = client.index(
        index = index_name,
        body = document,
        id = id,
        refresh = True
    )

    print('\nAdding document:')
    print(response)

    return response

def delete_index(index_name):
    # Delete the index.
    response = client.indices.delete(
        index = index_name
    )

    print('\nDeleting index:')
    print(response)

def delete_document(id):
    # Delete the document.
    response = client.delete(
        index = index_name,
        id = id
    )

    print('\nDeleting document:')
    print(response)


# ===========================================
#                  FLASK
# ===========================================

app = Flask(__name__)

@app.route('/add/<title>/<director>/<year>')
def add(title, director, year):
    
    # Add a document to the index.
    document = {
    'title': title,
    'director': director,
    'year': year
    }
    
    return add_document(document)

@app.route('/search/<term>')
def search(term):
    # Search for the document.        
    return search_fn(term)

@app.route('/delete/<id>')
def delete(id):
    # Delete a document.        
    return delete_document(id)

if __name__ == '__main__':
    init()
    app.run(debug=True)