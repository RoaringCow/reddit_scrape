import praw
import time
import json
import matplotlib.pyplot as plt

def authenticate(client_id="", client_secret="", user_agent=""):
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )
    return reddit

def get_subreddit():
    subreddit_name = "Turkey"  # input("Subreddit name?: ")
    subreddit = reddit.subreddit(subreddit_name)
    return subreddit


def get_post_comments(reddit, post_id):
    submission = reddit.submission(id=post_id)
    submission.comments.replace_more(limit=None)  # Retrieve all comments, including nested ones
    comments = submission.comments.list()
    return comments


def run_bot(reddit, post_count, subreddit):
    current_post = 0
    words_dict = {}
    # post_words_dict = {} will be used later on
    # comment_count = 0
    request_count = int(post_count / 100) + 1
    for x in range(request_count):  # Calculate how many requests are needed
        timer = time.time()
        posts = subreddit.new(limit=100, params={'before': 100 * x})  # Get the posts
        for post in posts:
            # Split the post title into words
            words = post.title.split()

            # Count the words
            for word in words:
                word = word.lower()
                if word in words_dict:
                    words_dict[word] += 1
                else:
                    words_dict[word] = 1

            current_post += 1
        print(f"{x + 1}th package done")
        # I might use this so i wont delete it
        #while time.time() - timer < 13:  # This value can be changed but when i tested without delay it got every 11 sec
            #print(f"Max request. Waiting... {int(13 - (time.time() - timer))} seconds")
            #time.sleep(13 - (time.time() - timer))
    return words_dict


reddit = authenticate(client_id="305yTJBnPYTaRE25kZ0Miw",
                      client_secret="uCVcPtnnOdgqEZ7ss_wjidWV1_z1-A",
                      user_agent="Oha")

words = run_bot(reddit, 100, get_subreddit())
words = dict(sorted(words.items(), key=lambda x: x[1], reverse=True))
with open("data.json", "w",  encoding="utf-8-sig") as file:
    json.dump(words, file, indent=4, ensure_ascii=False)

# Limit to 20 characters to make it not flood
keys = list(words.keys())[:20]
values = list(words.values())[:20]

plt.bar(keys, values, width=0.8)

# Set labels and title
plt.xlabel('Keys')
plt.ylabel('Values')
plt.title('Dictionary Values (First 20)')

# Rotate the x-axis labels vertically
plt.xticks(rotation='vertical')

# Display the plot
plt.show()