import praw
import os
import logging
from dotenv import load_dotenv
from src.comment_processor import CommentProcessor


class RedditBot:
  def __init__(self):
    load_dotenv()

    self.comment_processor = CommentProcessor()

    self.reddit = praw.Reddit(
        user_agent=os.getenv("USERNAME"),
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        username=os.getenv("USERNAME"),
        password=os.getenv("PASSWORD")
    )

    self.user_blacklist = [os.getenv("USERNAME"), "AutoModerator"]

  def monitor_reddit(self, subreddit_name):
    subreddit = self.reddit.subreddit(subreddit_name)

    print(f"Monitoring comments on r/{subreddit_name}")

    for comment in subreddit.stream.comments():
      if comment.author in self.user_blacklist:
        continue
      self.process_comment(comment)

  def process_comment(self, comment):
    try:
      self.comment_processor.process_text(comment.body, f"u/{comment.author}")
    except Exception as ex:
      logging.error(logging.traceback.format_exc())
