import urllib
import json
import logging


def quote(text):
    try:
        return urllib.quote(text.encode('utf-8'))
    except UnicodeDecodeError:
        return urllib.quote(unicode(text, 'utf-8').encode('utf-8'))


def quote_plus(text):
    try:
        return urllib.quote_plus(text.encode('utf-8'))
    except UnicodeDecodeError:
        return urllib.quote_plus(unicode(text, 'utf-8').encode('utf-8'))


def get(url):
    try:
        return urllib.urlopen(url).read()
    except urllib.error.HTTPError as err:
        logging.error(err)


def ajax(url):
    data = get(url)

    if data:
        logging.info('got data from ' + url)
        logging.info(data)

        try:
            return json.loads(data)
        except ValueError as err:
            logging.error(err)
