import json
import ssl
import pprint
import sys

from OpenSSL import crypto

pp = pprint.PrettyPrinter(indent=4)

# Python 3 does not have ssl.PROTOCOL_SSLv2
try:                                        # pragma: no cover
    extra_versions = [ssl.PROTOCOL_SSLv2]   # pragma: no cover
except AttributeError:                      # pragma: no cover
    extra_versions = [ssl.PROTOCOL_TLSv1_1,  # pragma: no cover
                      ssl.PROTOCOL_TLSv1_2]  # pragma: no cover

ssl_versions = [
    ssl.PROTOCOL_SSLv3,
    ssl.PROTOCOL_TLSv1,
    ssl.PROTOCOL_SSLv23
]

ssl_versions.extend(extra_versions)


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
    pp.pprint(get_remote_cert(sys.argv[1]))
