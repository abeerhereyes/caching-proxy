The server forwards requests to the actual server, caches the responses, and returns the cached response if the same request is made again. This reduces the load on the origin server and improves response times for repeated requests.

##
To start the caching proxy server, run the following command:
```
python main.py start --port <number> --origin <url>
```
##
To clear the cache rum :
```
 python main.py clear-cache 
```


##
https://roadmap.sh/projects/caching-server
