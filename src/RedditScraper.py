import praw
import argparse
import xml.etree.cElementTree as et


def main(community, numPosts):
    limit = int(numPosts)
    
    redditRead = praw.Reddit(client_id="xxxxxxxxxxxxxx", 
                            client_secret="xxxxxxxxxxxxxx",
                            user_agent="Scraped")
    
    subreddit = redditRead.subreddit(community)
    root = et.Element(subreddit.display_name)
    
    for post in subreddit.hot(limit=limit):
        if(post.stickied):
            limit+=1
            continue

        # submission = redditRead.submission(post.url)
        listing = et.SubElement(root, "title", title=post.title)
        et.SubElement(listing, "text", text=post.selftext)
        
        tree = et.ElementTree(root)
        tree.write(f"YoutubeShorts/xml/{community}.xml")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--subrredit", help='subreddit/community', required=True)
    parser.add_argument("--numPosts", help="how many posts to record", required=True)
    args = parser.parse_args()

    main(args.subrredit, args.numPosts)
