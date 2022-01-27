import requests
from tqdm import tqdm
import pandas as pd
import praw
from datetime import datetime
print("Packages Imported")

reddit = praw.Reddit(
        user_agent="Datashlurper (by u/RiceKrispySawdust)",
        client_id="z-vJvTo8CAiqqtDMazFE1Q",
        client_secret="ps1L9pw2RBF2wnGrlRea32CNw3Rr6w",
)

subreddit = "memes"
num_posts = 2000

df = pd.DataFrame(columns=[
    "post_id",
    "post_name",
    "title",
    "weekday",
    "top_comment",
    "num_comments",
    "upvotes",
    "downvotes",
    "upvote_ratio",
    "spoiler",
    "edited",
    "original",
    "over_18",
    "is_self",
    "img_url",
])

rows = []

posts = reddit.subreddit(subreddit).top(limit=num_posts, time_filter="year")
index = 0
for post in tqdm(posts):
    post_id = post.id
    post_name = post.name
    edited = post.edited
    original = post.is_original_content
    over_18 = post.over_18
    is_self = post.is_self
    num_comments = post.num_comments
    img_url = post.url
    upvotes = post.score
    # no memes have text on the post
    # text = post.selftext
    spoiler = post.spoiler
    upvote_ratio = post.upvote_ratio
    downvotes = round(upvotes/upvote_ratio) - upvotes
    title = post.title

    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    day_of_week = day_names[datetime.fromtimestamp(post.created_utc).weekday()]

    # get top comment
    post.comment_sort = "top"
    commentIndex = 0
    topComment = post.comments[commentIndex]
    while(topComment.stickied):
        commentIndex += 1
        topComment = post.comments[commentIndex]

    topComment = topComment.body

    rows.append([post_id, post_name, title, day_of_week, topComment, num_comments, upvotes, downvotes, upvote_ratio, spoiler, edited, original, over_18, is_self, img_url])

    # save image to folder

    img_data = requests.get(img_url).content
    filename = './images/' + str(index)
    extension = '.' + str(img_url).split('.').pop()
    # some images have no extension, which will result in a really long extension variable (e.g. '.it/fk9xpew8wnl71')
    # in these cases, 
    if(len(extension) > 6):
        extension = ""
    
    with open(filename + extension, 'wb') as handler:
        handler.write(img_data)
    
    index +=1 


for i in range(0, len(rows)):
    df.loc[i] = rows[i]

df.to_csv('reddit_memes.csv')
print("Reddit scrape complete.")
