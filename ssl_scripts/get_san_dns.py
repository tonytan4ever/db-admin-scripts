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


def get_ssl_number_of_hosts(remote_host):
    '''Get number of Alternative names for a (SAN) Cert

    '''

    for ssl_version in ssl_versions:
        try:
            cert = ssl.get_server_certificate((remote_host, 443),
                                              ssl_version=ssl_version)
        except ssl.SSLError:
            # This exception m
            continue

        x509 = crypto.load_certificate(crypto.FILETYPE_PEM, cert)

        sans = []
        for idx in range(0, x509.get_extension_count()):
            extension = x509.get_extension(idx)
            if extension.get_short_name() == 'subjectAltName':
                sans = [san.replace('DNS:', '') for san
                        in str(extension).split(',')]
                break

        # We can actually print all the Subject Alternative Names
        # for san in sans:
        #   print san
        result = len(sans)
        break
    else:
        raise ValueError('Get remote host certificate info failed...')
    return result


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: %s <remote_host_you_want_get_cert_on>' % sys.argv[0])
        sys.exit(0)
    print("There are %s DNS names for SAN Cert on %s" % (
        get_ssl_number_of_hosts(sys.argv[1]), sys.argv[1]))
