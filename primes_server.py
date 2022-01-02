#!/usr/bin/env python3
# Basic prime number service.
# Example invocation
# $ python3 -B primes_server.py
# $ ./grpc_cli ls localhost:50051
# $ ./grpc_cli ls localhost:50051 primes.Primes
# $ ./grpc_cli call localhost:50051 primes.Primes.Sieve 'hi: 150'
import argparse
import concurrent
import logging
import sys

import grpc
from grpc_reflection.v1alpha import reflection
import primes
import primes_pb2
import primes_pb2_grpc

from collections.abc import Sequence

def main(argv: Sequence[str]) -> int:
    """Server main."""
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument("--port", metavar='PORT', type=int,
                        dest='port', default=50051,
                        help='Port number on which to serve.')
    parser.add_argument("-v","--verbose",
                        dest='verbose', action="store_true",
                        help="run verbosely")
    args = parser.parse_args(args=argv[1:])
    if args.verbose:
        logging.getLogger().setLevel(logging.INFO)
        logging.info('port: %d', args.port)
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=4))
    primes_pb2_grpc.add_PrimesServicer_to_server(Primes(), server)
    SERVICE_NAMES = (
        primes_pb2.DESCRIPTOR.services_by_name['Primes'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port(f'localhost:{args.port}')
    server.start()
    server.wait_for_termination()
    return 0

class Primes(primes_pb2_grpc.PrimesServicer):
    """Service implementation."""
    def Sieve(self, request: primes_pb2.SieveRequest,
              context) -> primes_pb2.SieveResponse:
        sieve_result = primes.sieve(request.hi)
        response = primes_pb2.SieveResponse()
        response.p[:] = sieve_result
        return response

if __name__ == '__main__':
    sys.exit(main(sys.argv))
    
