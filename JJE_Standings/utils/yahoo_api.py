from oauthlib.common import generate_nonce, generate_timestamp
from oauthlib.oauth1.rfc5849 import signature
from urllib import parse

import requests

from JJE_Standings.models import YahooKey

prx = None
# from urllib import request as rq
# prx = {
#     'http': "http://barracuda:3128",
#     'https': "https://barracuda:3128"
# }
# proxy = rq.ProxyHandler(proxies = prx)
# opener = rq.build_opener(proxy)
# rq.install_opener(opener)

def save_yahoo_token(access_token, access_secret, session_handle):
    """Save the yahoo token"""
    token = YahooKey.objects.first() #type: YahooKey
    token.access_token = access_token
    token.access_secret_token = access_secret
    token.session_handle = session_handle
    token.save()


def refresh_yahoo_token():
    """Refreshes the yahoo token for the standings api"""

    token = YahooKey.objects.first()  # type: YahooKey

    # if not token.expired:
    #     return

    url = 'https://api.login.yahoo.com/oauth/v2/get_token'

    nonce = generate_nonce()
    timestamp = generate_timestamp()
    ck = token.consumer_key
    cks = token.consumer_secret
    ac = token.access_token
    acs = token.access_secret_token
    sh = token.session_handle
    sig_method = 'HMAC-SHA1'

    params = [('oauth_nonce', nonce,),
              ('oauth_consumer_key', ck,),
              ('oauth_signature_method', sig_method,),
              ('oauth_timestamp', u'{}'.format(timestamp),),
              ('oauth_version', u'1.0',),
              ('oauth_token', ac,),
              ('oauth_session_handle', sh,)]

    nparams = signature.normalize_parameters(params)

    oauth_sig_US = sign_request(cks, acs, url, nparams)

    params.append(('oauth_signature', oauth_sig_US))
    nparams = signature.normalize_parameters(params)

    if prx is not None:
        res = requests.get("{}?{}".format(url, nparams), proxies=prx)
    else:
        res = requests.get("{}?{}".format(url, nparams))

    res_final = convert_result(res)
    save_yahoo_token(
        res_final["oauth_token"],
        res_final["oauth_token_secret"],
        res_final["oauth_session_handle"]
    )

    return


def sign_request(client_secret, token_secret, url, nparams):
    """Sign the supplied request"""
    normalized_uri = signature.normalize_base_string_uri(url, None)
    base_string = signature.construct_base_string(u"GET", normalized_uri, nparams)
    sig = signature.sign_hmac_sha1(base_string, client_secret, token_secret)
    return u"{}".format(sig)


def convert_result(result):
    rs = result.text.split("&")
    data_dct = {}
    for item in rs:
        a, b = item.split("=")
        data_dct[a] = parse.unquote(b)
    return data_dct


