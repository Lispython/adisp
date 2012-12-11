'''
Artificial dumb example showing the essence of adisp. It read the contens from
a number of urls and prints the length of the responses. Asynchronous calls are
implemented using threads for simplicity.

'''
import threading
import urllib2

from adisp import async, process

@async
def get_url(url, callback):
    '''
    Asynchronous function. Starts a thread that will read the url and call
    the callback with the result.
    '''
    def read():
        callback(urllib2.urlopen(url).read())
    threading.Thread(target=read).start()

@process
def process_url():
    '''
    Calling process. Calls asynchronous get_url as a single call and as
    multiple calls.

    Note that call to process_call exits immediately and lets the main code
    to execute before it waits for threads.
    '''
    urls = ['http://google.com/', 'http://softwaremaniacs.org/']

    # Single call
    response = yield get_url(urls[0])
    print len(response), urls[0]

    # Multiple calls
    responses = yield map(get_url, urls)
    print '\n'.join('%s %s' % (len(r), u) for u, r in zip(urls, responses))

    # Multiple calls with empty list
    responses = yield map(get_url, [])
    if responses == []:
        print 'Empty list'

if __name__ == '__main__':
    process_url()
    print 'process_url returns before any results are available'
