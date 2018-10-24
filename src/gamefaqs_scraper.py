#
# gamefaqs-scraper
# github.com/01mu
#

import urllib2
from lxml import html

class GFSBoard:
    ''' Get thread information for a specific board '''
    class BoardThread:
        ''' Attributes for thread from a given board '''
        def __init__(self, title, author, last, replies, link):
            self.title = title
            self.author = author
            self.last = last
            self.replies = replies
            self.link = link

    ''' Get thread information for a specific board '''
    def get_max_page(self):
        ''' Get max page pagination option from thread list '''
        a = self.data.find('</select> of ') + 13
        less = self.data[a : ]
        b = less.find('<')
        self.max_page = int(less[ : b]) - 1

    def get_thread_pcount(self):
        ''' Get number of replies to thread '''
        counts = []
        hay = self.data

        while hay.find('<tr class="topics">') != -1:
            count_loc = hay.find('<td class="count">') + 18
            less = hay[count_loc : ]
            end_loc = less.find('</td>')
            fin = less[ : end_loc]
            counts.append(fin)
            hay = hay[count_loc :]

        return counts

    def get_thread_info(self, needle):
        ''' Get thread info for a specific thread attribute '''
        attrs = []
        hay = self.data
        length = len(needle)

        while hay.find('<tr class="topics">') != -1:
            f = hay.find(needle) + (length - 1)
            hay = hay[f : ]
            end_loc = hay.find('>')
            fin = hay.find('</a>', end_loc)
            e = hay[end_loc + (length) : fin]
            attribute = e[e.find('>') + 1 : ]
            attrs.append(attribute)

        return attrs

    def get_thread_links(self):
        ''' Get location of thread link for each thread from boards page '''
        links = []
        hay = self.data

        while hay.find('<tr class="topics">') != -1:
            topic_loc = hay.find('<td class="topic">') + 18
            less = hay[topic_loc : ]
            end_loc = less.find('>') + 1
            fin = less[ : end_loc]
            links.append(self.trim_thread_link(fin))
            hay = hay[topic_loc :]

        return links

    def trim_thread_link(self, link):
        ''' Remove HTML markup and return link to thread '''
        return link[link.find('"/boards') + 9 : len(link) - 2]

    def find(self):
        ''' Find thread attributes '''
        threads = []

        topics = self.get_thread_info('<td class="topic">')
        authors = self.get_thread_info('<td class="tauthor">')
        lasts = self.get_thread_info('<td class="lastpost">')
        replies = self.get_thread_pcount()
        links = self.get_thread_links()

        for i in range(len(topics)):
            thread = self.BoardThread(topics[i], authors[i], lasts[i],
                replies[i], links[i])
            threads.append(thread)

        return threads

    def get_site(self, board, page):
        ''' Get site text with board and page '''
        self.board = board
        url = self.BASE_URL + board + '?page=' + str(page)
        request = urllib2.Request(url)
        request.add_header('User-Agent', self.USER_AGENT)
        self.data = urllib2.urlopen(request).read()

        '''with open('board', 'r') as myfile:
            self.data = myfile.read()'''

        self.get_max_page()

    def __init__(self):
        ''' Initialize with base URL and user agent '''
        self.USER_AGENT = 'Mozilla/5.0'
        self.BASE_URL = 'https://gamefaqs.gamespot.com/boards/'

class GFSThread:
    ''' Get thread posts '''
    class ThreadPost:
        ''' Post info for a thread '''
        def __init__(self, author, date, body):
            self.author = author
            self.date = date
            self.body = body

    def get_max_page(self):
        ''' Get max page pagination option from thread list '''
        pag = '<ul class="paginate"><li>Page '
        a = self.data.find(pag) + len(pag)
        less = self.data[a : ]
        b = less.find('<')
        self.max_page = (less[ less[ : b].rfind(" ") + 1 : b])

    def get_info(self, needle, end):
        ''' Get info for a specific thread attribute (author or date) '''
        attrs = []
        hay = self.data
        length = len(needle) + 1

        while hay.find('class="name menu_toggle">') != -1:
            f = hay.find(needle) + (length - 1)
            end_loc = hay[f : ].find(end)
            attrs.append(hay[f : f + end_loc])
            hay = hay[f + length : ]

        return attrs

    def find(self):
        ''' Find post attributes '''
        posts = []
        authors = self.get_info('class="name menu_toggle"><b>', '</b>')
        dates = self.get_info('<span class="post_time" title="', '">')
        bodies = self.get_posts()
        self.trim_date(dates)

        for i in range(len(authors)):
            post = self.ThreadPost(authors[i], dates[i], bodies[i])
            posts.append(post)

        return posts

    def trim_date(self, dates):
        ''' Remove &nbsp; from dates '''
        for i in range(len(dates)):
            dates[i] = dates[i].replace("&nbsp;", " ")

    def get_posts(self):
        ''' Remove citations (quotes) '''
        posts = []
        msg = '<div class="msg_body_box"'
        hay = self.data

        while hay.find(msg) != -1:
            f = hay.find(msg)
            thing = hay[f : ].find('</div><div class="msg_below_clear">')
            post = hay[f : f + thing]
            get = post.rfind(">") + 1
            posts.append(post[get : ].replace("\n", ""))
            hay = hay[f + thing : ]

        return posts

    def remove_breaks(self):
        ''' Trim line breaks '''
        self.data = self.data.replace("<br />", " ")

    def remove_poll(self):
        ''' Check if the OP includes a poll and remove it '''
        pos = self.data.find('<div class="board_poll">')

        if pos != -1:
            end_loc = self.data[pos : ].find('<div class="poll_foot">')
            self.data = self.data[ : pos] + self.data[pos + end_loc : ]

    def remove_signatures(self):
        ''' Remove signatures from posts '''
        sig = '<div class="signature"><div class="sig_text">'
        end = '</div></div>'
        hay = self.data

        while hay.find(sig) != -1:
            f = hay.find(sig)
            thing = hay[f : ].find(end)
            hay = hay[ : f ] + hay[f + thing + len(end) : ]

        self.data = hay

    def get_site(self, thread, page):
        ''' Get site text with board and page '''
        url = self.BASE_URL + thread + '?page=' + str(page)
        request = urllib2.Request(url)
        request.add_header('User-Agent', self.USER_AGENT)
        self.data = urllib2.urlopen(request).read()

        '''with open('thread', 'r') as myfile:
            self.data = myfile.read()'''

        self.remove_breaks()
        self.remove_poll()
        self.remove_signatures()
        self.get_max_page()

    ''' Posts and authors for a given thread '''
    def __init__(self):
        ''' Get thread URL '''
        self.USER_AGENT = 'Mozilla/5.0'
        self.BASE_URL = 'https://gamefaqs.gamespot.com/boards/'
