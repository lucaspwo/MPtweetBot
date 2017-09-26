# Twitter bot for MicroPython v1.8.4 (ESP8166)
#
# Copyright (c) 2016, Atsushi Yokoyama, Firmlogics (http://flogics.com)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#     * Neither the name of the <organization> nor the names of its
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT
# HOLDER> BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

global CK
global CS
global AT
global AS

def current_time():
    import time
    t = time.time()
    return t + 946684800

def enc_percent(s):
    ret = ''
    for c in s:
        ordc = ord(c)
        if ordc in range(0x30, 0x39 + 1) or \
           ordc in range(0x41, 0x5a + 1) or \
           ordc in range(0x61, 0x7a + 1) or \
           ordc in (0x2d, 0x2e, 0x5f, 0x7e):
            ret += c
        else:
            ret += '%%%02X' % (ordc)
    return ret

def oauth_sign(method, url, s, vcs, vas):
    import hmac
    import ubinascii
    import uhashlib

    str = ''
    for t in sorted(s):
        if str != '':
            str += '&'
        str += "%s=%s" % (t[0], enc_percent(t[1]))
    str = "%s&%s&%s" % (method.upper(), enc_percent(url), enc_percent(str))
    signing_key = bytearray(enc_percent(vcs) + '&' + enc_percent(vas))
    hash = hmac.new(signing_key, msg=str, digestmod=uhashlib.sha1)
    ret = ubinascii.b2a_base64(hash.digest()).rstrip()
    return ret

def oauth_genhead(vck, vcs, vat, vas, status):
    import ubinascii
    import os

    tstamp = current_time()
    nonce = 'nonce%d' % (tstamp)
    pairs = {
        ('status', status),
        ('include_entities', 'true'),
        ('oauth_consumer_key', vck),
        ('oauth_nonce', nonce),
        ('oauth_signature_method', 'HMAC-SHA1'),
        ('oauth_timestamp', str(tstamp)),
        ('oauth_token', vat),
        ('oauth_version', '1.0')}

    sig = oauth_sign('POST', \
          'https://api.twitter.com/1.1/statuses/update.json', \
          pairs, vcs, vas).decode('utf-8')

    s = '''        OAuth oauth_consumer_key="%s", 
              oauth_nonce="%s", 
              oauth_signature="%s", 
              oauth_signature_method="HMAC-SHA1", 
              oauth_timestamp="%d", 
              oauth_token="%s", 
              oauth_version="1.0"''' % \
        (vck, nonce, enc_percent(sig), tstamp, vat)
    return s

def tweet(s):
    global CK
    global CS
    global AT
    global AS
    body = 'status=%s' % (enc_percent(s))
    oauth_head = oauth_genhead(CK, CS, AT, AS, s)
    header = '''POST /1.1/statuses/update.json?include_entities=true HTTP/1.1
Accept: */*
Connection: close
User-Agent: TweetBot v0.2
Content-Type: application/x-www-form-urlencoded
Authorization: 
%s
Content-Length: %d
Host: api.twitter.com
''' % (oauth_head, len(body))
    return header + '\n' + body + '\n'

###############################################################################
def run(temp,umid):
    global CK
    global CS
    global AT
    global AS
    CK = 'gI1n0GzTcX0R45JrhtlHX0hbE'     # CONSUMER_KEY
    CS = 'tsVkeSOld0E5pXevGYdiOLSB4VsUHKKsxsjzHKgeM39HhiKhIZ'     # CONSUMER_SECRET
    AT = '31201720-x9NSSP36E1e8eZRz0bsdI5by9pm94E00E11NUXvY1'     # ACCESS_KEY
    AS = 'zojx7oNunlDe3gtJsDMzDwREdmTBRLcu9tgQoFzdbFImu'     # ACCESS_SECRET

    # time_diff = -3 * 3600                                        # Time difference

    # import time
    import ntptime

    while True:
        try:
            ntptime.settime()
            break
        except:
            pass

    # t = time.localtime(time.time() + time_diff)
    # t = time.localtime(time.time())
    # time_str = '%02d/%02d/%02d %02d:%02d:%02d' % t[0:6]
    # tweet_status = 'Pot plant needs water (%s)' % (time_str)
    # tweet_status = 'Teste de tweet a partir do ESP8266. Data atual: (%s)' % (time_str)
    tweet_status = 'Temperatura: %dC. Umidade: %d%%' % (temp, umid)
    s = tweet(tweet_status)
    f = open('tweet.txt', 'w')
    f.write(s)
    f.close()

def send():
    f = open('tweet.txt').read()
    # str = f.read(4096)
    # f.close()

    import usocket
    import ussl
    s=usocket.socket()
    addr = usocket.getaddrinfo("api.twitter.com", 443)[0][-1]
    s.connect(addr)
    s=ussl.wrap_socket(s)
    # print(s)
    s.write(f)
    # print(s.read(4096))
    s.close()
    rm_tweet_txt()

def rm_tweet_txt():
    import os
    os.remove('tweet.txt')