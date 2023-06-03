import praw
import json
import time

def count_words(subreddit_name, limit=None, skip=0, word_counts={}, post_count=0):
    # Authenticate with the Reddit API
    with open("user_data.json", "r") as json_file:
        credentials = json.load(json_file)

    # Access the values
    client_id = credentials["client_id"]
    client_secret = credentials["client_secret"]
    user_agent = credentials["user_agent"]

    # Use the values
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

    # Get the subreddit
    subreddit = reddit.subreddit(subreddit_name)

    # Get the newest posts in the subreddit
    posts = subreddit.new(limit=limit, params={'before': skip})

    # Iterate over the posts in the subreddit
    for post in posts:
        # Split the post title into words
        words = post.title.split()

        # Update the word counts
        for word in words:
            word = word.lower()
            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1
        post_count += 1

        percentage = post_count * 100 / (total_posts_to_fetch * number_of_requests)
        # print how much is done
        print(f"%{percentage} done")

    return post_count, word_counts


subreddit_name = 'Turkey'
total_posts_to_fetch = 100  # Set the total number of posts you want to fetch
skip = 0  # Skip the posts that have already been looked at
post_count = 0
word_counts = {}  # Words are stored here
number_of_requests = 12
REQUEST_LIMIT = 60  # reddit api allows only 60 per minute
current_request_count = 0
timer = time.time()  # to reset current request count

# Iterate not to exceed the single request limit which I saw was around 900 posts
for x in range(number_of_requests):
    while current_request_count > 60:  # wait until the time is reset
        if timer - time.time() > 60:  # reset count every 60 seconds
            current_request_count = 0
            timer = time.time()

    post_count, word_counts = count_words(subreddit_name, limit=total_posts_to_fetch, skip=skip,
                                          word_counts=word_counts, post_count=post_count)
    skip += total_posts_to_fetch
    current_request_count += 1  # add 1 every iteration

# sort
word_counts = dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True))
print("Total number of posts:", post_count)
print("Word counts:", word_counts)
# json_object = json.dumps(word_counts, indent = 4, ensure_ascii=False)
# print(json_object)

with open("data.json", "w",  encoding="utf-8-sig") as file:
    json.dump(word_counts, file, indent=4, ensure_ascii=False)  # ensure_ascii is to preserve some characters