import json
import ssl
import sys

import M2Crypto


ssl_versions = [
    ssl.PROTOCOL_SSLv3,
    ssl.PROTOCOL_TLSv1,
    ssl.PROTOCOL_SSLv2,
    ssl.PROTOCOL_SSLv23
]


def get_remote_cert(remote_host):
    for ssl_version in ssl_versions:
        try:
            cert = ssl.get_server_certificate((remote_host, 443),
                                              ssl_version=ssl_version)
        except ssl.SSLError:
            # This exception m
            continue
        x509 = M2Crypto.X509.load_cert_string(cert)

        result = {
            "pemEncodedCert": str(cert),
            "sha1Fingerprint": x509.get_fingerprint('sha1')
        }
        break
    else:
        raise ValueError('Get remote host certificate info failed...')
    return json.dumps(result)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: %s <remote_host_you_want_get_cert_on>' % sys.argv[0])
    print(get_remote_cert(sys.argv[1]))
