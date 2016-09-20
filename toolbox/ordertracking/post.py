# -*- coding: utf-8 -*-
from urllib2 import urlopen
from bs4 import BeautifulSoup
from collections import OrderedDict
from toolbox.settings import TRACK_TRACE_LANGUAGE


class TrackAndTrace(object):
    '''
    Track & Trace class for post.ch.
    '''

    @classmethod
    def request(cls, numbers):
        '''
        Sends the HTTP request to the post.ch Track & Trace site.
        '''
        # Build URL for Post.
        url = 'https://www.post.ch/swisspost-tracking'
        url += '?formattedParcelCodes={}'.format(';'.join(numbers))
        url += '&p_language={}'.format(TRACK_TRACE_LANGUAGE)

        # Fetch site.
        fh   = urlopen(url)
        html = fh.read()
        fh.close()

        # Return fetched HTML content.
        return html

    @classmethod
    def parse(cls, html):
        '''
        Parses the received HTML content from the post.ch Track & Trace site
        and returns the shipping numbers and status in an ordered dict.
        '''
        parser    = BeautifulSoup(html, 'html.parser')
        result    = parser.body.find('div', id='resultContent')
        numbers   = result.find_all('span', attrs={'class': 'shipmentNumber'})
        events    = result.find_all('td', attrs={'class': 'fvEvent'})

        numbers   = map(lambda x: x.string.strip(), numbers)
        events    = map(lambda x: x.string.strip(), events)

        count     = len(numbers)
        shipments = []

        for i in range(count):
            shipments.append((numbers[i], events[i]))

        return shipments

    @classmethod
    def get_shipping_events(cls, numbers):
        '''
        Takes a bunch of shipping numbers and returns the latest Track & Trace
        informations in a dict.
        '''
        # Make sure numbers is a list and not a string.
        if isinstance(numbers, basestring):
            numbers = [numbers]

        # Numbers with only 3 characters will result to an error, so remove them.
        numbers = filter(lambda x: len(x) >= 4, numbers)

        # Split numbers into chunks, because only 20 numbers are allowed.
        chunks = []
        while numbers:
            chunks.append(numbers[:20])
            del numbers[:20]

        # Now fetch all the events.
        events = []
        for numbers in chunks:

            # Request HTML content.
            html = cls.request(numbers)

            # Parse HTML content and return infos.
            events += cls.parse(html)

        return OrderedDict(events)
