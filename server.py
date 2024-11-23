from flask import Flask, request, Response
from cachetools import TTLCache
import requests
from urllib.parse import urljoin

cache = TTLCache(maxsize=100, ttl=300)  # Cache with 100 entries, 5 min TTL

def start_server(port, origin):
    app = Flask(__name__)

    @app.route('/', defaults={'path': ''}, methods=['GET'])
    @app.route('/<path:path>', methods=['GET'])
    def proxy(path):
        # Build the cache key and URL
        cache_key = request.full_path
        target_url = urljoin(origin, path) + ('?' + request.query_string.decode() if request.query_string else '')

        # Check if the response is cached
        if cache_key in cache:
            cached_response = cache[cache_key]
            response = Response(
                cached_response['data'], 
                status=cached_response['status_code']
            )
            for header, value in cached_response['headers'].items():
                response.headers[header] = value
            response.headers['X-Cache'] = 'HIT'
        else:
            try:
                # Fetch the response from the origin server
                upstream_response = requests.get(target_url)
                upstream_response.raise_for_status()  # Raise an exception for bad responses

                # Cache the response
                cache[cache_key] = {
                    'data': upstream_response.content,
                    'status_code': upstream_response.status_code,
                    'headers': dict(upstream_response.headers)
                }

                # Construct the Flask response
                response = Response(
                    upstream_response.content, 
                    status=upstream_response.status_code
                )
                for header, value in upstream_response.headers.items():
                    response.headers[header] = value
                response.headers['X-Cache'] = 'MISS'
            except requests.RequestException as e:
                # Return a 502 Bad Gateway if the upstream request fails
                response = Response(f"Error fetching from origin: {str(e)}", status=502)
        print(response.headers['X-Cache'])
        return response

    @app.route('/favicon.ico')
    def favicon():
        return Response(status=204)  # No content for favicon

    app.run(port=port)




def clear_cache():
    cache.clear()
    print('Cache cleared')