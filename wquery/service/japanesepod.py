# -*- coding: utf-8 -*-
import json
import os
import re
import urllib
import urllib2
import xml.etree.ElementTree
from collections import defaultdict

from aqt.utils import showInfo

from .base import WebService, export, register
from wquery.odds import ignore_exception


@register(u'japanese')
class Japanesepod(WebService):

    def __init__(self):
        super(Japanesepod, self).__init__()


    # @ignore_exception
    @export(u'发音', 0)
    def fld_phonetic(self): 
        
        audio_name = 'jpod_%s.mp3' % self.word
        
        url = get_from_jisho(self.word)
        if not url:
            url = get_from_japod(self.word)
        if not url:
            return

        urllib.urlretrieve(url, audio_name)
        with open(audio_name, 'rb') as f:
            if f.read().strip() == '{"error":"Document not found"}':
                os.remove(audio_name)
                return ''
        return self.get_anki_label(audio_name, 'audio')


def get_from_jisho(word):
    quoted_query = urllib.quote(word.encode("utf-8"))
    url = u"http://jisho.org/search/%s" % (quoted_query)
    try:
        req = urllib2.Request(url.encode('utf-8')) 
        html = urllib2.urlopen(req).read()
        # print html
        raw_url = re.search(r'audio id=(.+?) type="audio/mpeg"', html).groups()[0]
        # print(raw_url)
        src_url = re.search(r'src="(.+)"', raw_url).groups()[0].replace("//", "")
        return "http://" + src_url
        # print(src_url)
    except:
        pass

def get_from_japod(word):
    url = u"https://www.japanesepod101.com/learningcenter/reference/dictionary_post"
    params = {u'post': u'dictionary_reference',
                    u'match_type': u'exact',
                    u'search_query': word.encode('utf-8')}
    headers={"User-Agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"}
    data = urllib.urlencode(params)
    req = urllib2.Request(url, data, headers)
    try:
        response = urllib2.urlopen(req)
        html = response.read()
    except:
        pass

    try:
        return re.search(r'data-url=\'(.+?)\' data-type', html).groups()[0]
    except:
        pass