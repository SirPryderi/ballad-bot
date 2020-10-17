# ballad-bot

## About

Ballad bot is a Reddit bot that detects various poetical formats in reddit comments, and replies to the thread with a poetically-formatted version of the comment.

It is strongly inspired from [RIP](https://github.com/pmichel31415/reddit-iambic-pentameter) and the slightly more famous [u/haikusbot](https://www.reddit.com/user/haikusbot/)

## Running

To run against a subreddit:

```sh
python main.py AskReddit
```

`all` is a valid option to watch the entire Reddit.

To run against local test data:

```sh
python main.py --test
```

## Requirements

It requires Python 3.8 (newer might work) and the packages declared in `requirements.txt`.