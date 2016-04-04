import sys
from tweet_processor import TweetProcessor

if __name__ == "__main__":
    input = sys.argv[1]
    output = sys.argv[2]
    processor = TweetProcessor()
    processor.execute(input, output)
