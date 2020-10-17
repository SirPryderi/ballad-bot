#!/usr/bin/python3.8

import os
import sys
from src.comment_processor import CommentProcessor
from src.reddit_bot import RedditBot


def run_from_file():
  comment_processor = CommentProcessor()
  dir = 'test_data/'
  entries = os.listdir(dir)
  for entry in entries:
    with open(dir + '/' + entry, 'r') as f:
      data = f.read()
      comment_processor.process_text(data)


if __name__ == '__main__':
  if '--test' in sys.argv:
    run_from_file()
  else:
    try:
      subreddit = sys.argv[1]
    except:
      subreddit = "ballad_bot_playground"

    bot = RedditBot()
    bot.monitor_reddit(subreddit)
