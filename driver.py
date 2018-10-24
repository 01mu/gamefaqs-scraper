#
# gamefaqs-scraper
# github.com/01mu
#

import urllib2
from lxml import html

class GFSBoard:
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

    def get_thread_info(self, needle, end, length):
        ''' Get thread info for a specific thread attribute '''
        attrs = []
        hay = self.data

        while hay.find('<tr class="topics">') != -1:
            f = hay.find(needle) + (length - 1)
            hay = hay[f : ]
            end_loc = hay.find('>')
            fin = hay.find(end, end_loc)
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
        return self.BASE_URL + link[link.find('"/boards') + 9 : len(link) - 2]

    def find(self):
        ''' Find thread attributes '''
        threads = []

        topics = self.get_thread_info('<td class="topic">', '</a>', 18)
        authors = self.get_thread_info('<td class="tauthor">', '</a>', 20)
        lasts = self.get_thread_info('<td class="lastpost">', '</a>', 21)
        replies = self.get_thread_pcount()
        links = self.get_thread_links()

        for i in range(len(topics)):
            thread = BoardThread(topics[i], authors[i], lasts[i], replies[i],
                links[i])

            threads.append(thread)

        return threads

    def get_site(self, board, page):
        ''' Get site text with board and page '''
        self.board = board
        url = self.BASE_URL + board + '?page=' + str(page)
        request = urllib2.Request(url)
        request.add_header('User-Agent', self.USER_AGENT)
        self.data = urllib2.urlopen(request).read()
        self.get_max_page()

    def __init__(self, board):
        ''' Initialize with base URL and user agent '''
        self.board = board
        self.USER_AGENT = 'Mozilla/5.0'
        self.BASE_URL = 'https://gamefaqs.gamespot.com/boards/'

class BoardThread:
    ''' Attributes for thread from a given board '''
    def __init__(self, title, author, last, replies, link):
        self.title = title
        self.author = author
        self.last = last
        self.replies = replies
        self.link = link

class GFSThread:
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

        self.trim_date(dates)

        self.remove_poll()
        self.remove_signatures()

        bodies = self.get_posts()

        for i in range(len(authors)):
            post = ThreadPost(authors[i], dates[i], bodies[i])

            posts.append(post)

        return posts

    def trim_date(self, dates):
        ''' Remove &nbsp; from dates '''
        for i in range(len(dates)):
            dates[i] = dates[i].replace("&nbsp;", " ")

    def get_posts(self):
        ''' Remove citations (quotes) '''
        posts = []
        hay = self.data

        while hay.find('<div class="msg_body_box"') != -1:
            f = hay.find('<div class="msg_body_box"')
            thing = hay[f : ].find('</div><div class="msg_below_clear">')
            post = hay[f : f + thing]
            get = post.rfind(">") + 1
            posts.append(post[get : ])
            hay = hay[f + thing : ]

        return posts

    def remove_signatures(self):
        ''' Remove signatures from posts '''
        hay = self.data

        while hay.find('<div class="signature"><div class="sig_text">') != -1:
            f = hay.find('<div class="signature"><div class="sig_text">')
            thing = hay[f : ].find('</div></div>')
            hay = hay[ : f ] + hay[f + thing + len('</div></div>') : ]

        self.data = hay

    def remove_poll(self):
        ''' Check if the OP includes a poll and remove it '''
        pos = self.data.find('<div class="board_poll">')

        if pos != -1:
            end_loc = self.data[pos : ].find('<div class="poll_foot"></div>')
            self.data = self.data[ : pos] + self.data[pos + end_loc + 51 : ]

    def get_site(self):
        ''' Get site text with board and page '''
        request = urllib2.Request(self.thread)
        request.add_header('User-Agent', self.USER_AGENT)
        self.data = urllib2.urlopen(request).read()

        #with open('site', 'r') as myfile:
        #    self.data = myfile.read()

    ''' Posts and authors for a given thread '''
    def __init__(self, thread):
        ''' Get thread URL '''
        self.thread = thread
        self.USER_AGENT = 'Mozilla/5.0'

class ThreadPost:
    ''' Post info for a thread '''
    def __init__(self, author, date, body):
        self.author = author
        self.date = date
        self.body = body


#gfs = GFSBoard('234547-super-smash-bros-ultimate')
#gfs.get_site('234547-super-smash-bros-ultimate', 0)
#threads = gfs.find()

thread = GFSThread('')
thread.get_site()
posts = thread.find()

for i in range(len(posts)):
    print(posts[i].author)
    print(posts[i].date)
    print(posts[i].body)
