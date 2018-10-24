# gamefaqs-scraper
Scrape board and thread information from GameFAQs. Repeated use leads to a temporary IP block from GameFAQs.

## Get threads from a board
### Input (`driver.py`):
```python
from gamefaqs_scraper import GFSBoard

board = GFSBoard()
board.get_site('234547-super-smash-bros-ultimate', 0)
threads = board.find()

print("Pages: " + str(board.max_page) + "\n")

for i in range(len(threads)):
    print(threads[i].title + "\n" + threads[i].author + "\n" + threads[i].last
        + "\n" + threads[i].replies + "\n" + threads[i].link + "\n")
```
### Output:
```
Pages: <max pagination>

<Title>
<Author>
<Last post date>
<Post count>
<Link to thread>

<Title>
<Author>
...
```
## Get posts from a thread
### Input (`driver.py`):
```python
from gamefaqs_scraper import GFSThread

thread = GFSThread()
thread.get_site('234547-super-smash-bros-ultimate/77126753', 0)

posts = thread.find()

print("Pages: " + str(thread.max_page) + "\n")

for i in range(len(posts)):
    print(posts[i].author + "\n" + posts[i].date + "\n" + posts[i].body + "\n")
```
### Output:
```
Pages: <max pagination>

<Author>
<Post date>
<Post body>

<Author>
...
```
