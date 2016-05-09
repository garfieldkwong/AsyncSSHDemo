import argparse
import asyncio
import asyncssh
import sys
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicNumbers
print(dir(EllipticCurvePublicNumbers))


@asyncio.coroutine
def run_client(username, password):
    with (yield from asyncssh.connect(
        'localhost', username=username, password=password, known_hosts=None
    )) as conn:
        stdin, stdout, stderr = yield from conn.open_session('echo "Hello!"')

        output = yield from stdout.read()
        print(output, end='')

        yield from stdout.channel.wait_closed()

        status = stdout.channel.get_exit_status()
        if status:
            print('Program exited with status %d' % status, file=sys.stderr)
        else:
            print('Program exited successfully')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('username')
    parser.add_argument('password')
    args = parser.parse_args()
    asyncio.get_event_loop().run_until_complete(
        run_client(args.username, args.password)
    )
