from praw.models.reddit.comment import Comment
from src.poem import Poem
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
        user_agent=os.getenv("USER_AGENT"),
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        username=os.getenv("USERNAME"),
        password=os.getenv("PASSWORD")
    )

    self.user_blacklist = [os.getenv("USERNAME"), "AutoModerator"]
    self.dedicated_subreddit = self.reddit.subreddit("ballad_bot_playground")

  def monitor_reddit(self, subreddit_name: str):
    subreddit = self.reddit.subreddit(subreddit_name)

    print(f"Monitoring comments on r/{subreddit_name}")

    for comment in subreddit.stream.comments():
      if comment.author in self.user_blacklist:
        continue
      self.process_comment(comment)

  def post_to_dedicated_subreddit(self, poem: Poem, comment: Comment):
    print("[->] Posting to dedicated subreddit...")
    selftext = [
        f"{poem.to_markdown()}",
        "---",
        f"rhyme scheme: {''.join(poem.rhyme_scheme)} | score: {poem.score} | [see thread](https://reddit.com{comment.permalink})"
    ]
    selftext = "\n\n".join(selftext)

  def post_reply(self, poem: Poem, comment: Comment):
    print("[->] Replying to original comment...")
    body = [
        f"{poem.to_markdown()}",
        "---",
        f"rhyme scheme: {''.join(poem.rhyme_scheme)} | score: {poem.score}"
    ]
    body = "\n\n".join(body)
    comment.reply(body)

  def process_comment(self, comment: Comment):
    try:
      candidates = self.comment_processor.process_text(comment.body, author=f"u/{comment.author}")

      if len(candidates) == 0:
        return

      best_poem = max(candidates, key=lambda p: p.score)
      if best_poem.score > 140:
        self.post_to_dedicated_subreddit(best_poem, comment)
      if best_poem.score > 100:
        self.post_reply(best_poem, comment)

    except Exception as ex:
      logging.error(logging.traceback.format_exc())
