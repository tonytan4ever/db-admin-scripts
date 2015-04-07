import json
import ssl
import sys

from OpenSSL import crypto

# Python 3 does not have ssl.PROTOCOL_SSLv2
try:                             # pragma: no cover
    sslv2 = ssl.PROTOCOL_SSLv2   # pragma: no cover
except AttributeError:           # pragma: no cover
    sslv2 = None                 # pragma: no cover

ssl_versions = [
    ssl.PROTOCOL_SSLv3,
    ssl.PROTOCOL_TLSv1,
    ssl.PROTOCOL_SSLv23
]

if sslv2 is not None:            # pragma: no cover
    ssl_versions.append(sslv2)   # pragma: no cover


def get_remote_cert(remote_host):
    for ssl_version in ssl_versions:
        try:
            cert = ssl.get_server_certificate((remote_host, 443),
                                              ssl_version=ssl_version)
        except ssl.SSLError:
            # This exception m
            continue
        x509 = crypto.load_certificate(crypto.FILETYPE_PEM, cert)

        result = {
            "pemEncodedCert": str(cert),
            "sha1Fingerprint": x509.digest('sha1').replace(':','')
        }
        break
    else:
        raise ValueError('Get remote host certificate info failed...')
    return json.dumps(result)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: %s <remote_host_you_want_get_cert_on>' % sys.argv[0])
        sys.exit(0)
    print(get_remote_cert(sys.argv[1]))
