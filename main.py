import argparse
from server import start_server, clear_cache


def main():
    parser = argparse.ArgumentParser(
                        prog='caching Proxy',
                        description='Caches requests made to the server and responds from the cache when applicable.',
                        )
    subparser =parser.add_subparsers(dest='command')

    start_parser = subparser.add_parser('start', help='Start the caching proxy server')
    start_parser.add_argument('--port', type=int, default=5000, help='Port number (default: 5000)')

    start_parser.add_argument('--origin', type=str, required=True, help='Origin URL')

    clear_parser = subparser.add_parser('clear-cache', help='Clear the cache')

    args = parser.parse_args()
    if args.command == 'start':
        print(f"starting server... port is {args.port} and origin is {args.origin}")
        start_server(args.port, args.origin)

    elif args.command == 'clear-cache':
        print('clearing cache...')
        clear_cache()
if __name__ == "__main__":
    main()