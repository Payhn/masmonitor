from mastodon import Mastodon
import time
import json

# Register an app and get the client_id and client_secret
# Replace these with your own values from the registration process
client_id = "your_client_id"
client_secret = "your_client_secret"

# Log in to your Mastodon instance with your username and password
# Replace these with your own Mastodon credentials
username = "your_username"
password = "your_password"

# The instance URL
mastodon_instance_url = "https://mastodon.social"

# List of hashtags to monitor
hashtags_to_monitor = ["example1", "example2", "example3"]

# Create a Mastodon API instance
mastodon = Mastodon(
    client_id=client_id,
    client_secret=client_secret,
    access_token=None,
    api_base_url=mastodon_instance_url
)

# Log in to the Mastodon instance
access_token = mastodon.log_in(
    username,
    password,
    scopes=["read"]
)
mastodon.access_token = access_token

# Load seen posts data from a JSON file, or create an empty dictionary
try:
    with open("seen_posts.json", "r") as f:
        seen_posts = json.load(f)
except FileNotFoundError:
    seen_posts = {}

# Monitor the hashtags
while True:
    for hashtag in hashtags_to_monitor:
        # Fetch the latest posts with the hashtag
        posts = mastodon.timeline_hashtag(hashtag, limit=20)

        for post in posts:
            post_id = post["id"]
            if post_id not in seen_posts:
                # This is a new post
                print(f"New post with hashtag {hashtag}: {post['content']}")

                # Save the post info to the seen_posts dictionary
                seen_posts[post_id] = {"timestamp": post["created_at"], "content": post["content"]}

                # Save the updated seen_posts dictionary to the JSON file
                with open("seen_posts.json", "w") as f:
                    json.dump(seen_posts, f)

    # Wait for a while before checking for new posts again
    time.sleep(60)

