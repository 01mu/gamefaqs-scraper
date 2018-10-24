#
# gamefaqs-scraper
# github.com/01mu
#

from gamefaqs_scraper import GFSBoard
from gamefaqs_scraper import GFSThread

board = GFSBoard()
board.get_site('234547-super-smash-bros-ultimate', 0)
threads = board.find()

print("Pages: " + str(board.max_page) + "\n")

for i in range(len(threads)):
    print(threads[i].title + "\n" + threads[i].author + "\n" + threads[i].last
        + "\n" + threads[i].replies + "\n" + threads[i].link + "\n")

'''
thread = GFSThread()
thread.get_site('234547-super-smash-bros-ultimate/77126753', 0)

posts = thread.find()

print("Pages: " + str(thread.max_page) + "\n")

for i in range(len(posts)):
    print(posts[i].author + "\n" + posts[i].date + "\n" + posts[i].body + "\n")
'''
