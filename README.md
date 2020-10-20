# ballad-bot

## About

Hello, I'm [u/ballad-bot](https://reddit.com/u/ballad-bot), a Reddit bot that detects various structured poetical formats in comments, by analyzing the number of syllables, and replies to the thread with a poetically-formatted version of the same comment.

Think of me as the lovechild of [RIP](https://github.com/pmichel31415/reddit-iambic-pentameter) and the slightly more famous [u/haikusbot](https://www.reddit.com/user/haikusbot/).

## Known Issues
I'm pretty bad at detecting the meter at the moment. Something with the underlying pronouncing library is off and makes me very dumb.

## Running

If you intend or running me in bot mode, you first need to create a new `.env` file based on on `.example.env`.

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

I require Python 3.8 (newer might work) and the packages declared in `requirements.txt`.

## See also

Other (much cleverer) projects than me. I don't know even anything about poetry. There, I've said it. Check them out for a good code read.

- https://github.com/pmichel31415/reddit-iambic-pentameter
- https://github.com/hyperreality/Poetry-Tools
