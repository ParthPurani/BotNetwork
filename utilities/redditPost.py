import requests
from helpers.jsonUtils import *


def authenticateReddit(clientId, secret, userName, password):

    # note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
    auth = requests.auth.HTTPBasicAuth(clientId, secret)

    # here we pass our login method (password), username, and password
    data = {'grant_type': 'password',
            'username': userName,
            'password': password}

    # setup our header info, which gives reddit a brief description of our app
    headers = {'User-Agent': 'parthsredditbot/0.0.2'}

    # send our request for an OAuth token
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)

    # convert response to JSON and pull access_token value
    TOKEN = res.json()['access_token']

    # add authorization to our headers dictionary
    headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

    return headers


# this function should get top post and comment
def get_postData(headers, subreddits):

    # while the token is valid (~2 hours) we just add headers=headers to our requests
    requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

    posts = []
    for subreddit in subreddits:
        # Get the post and retrive top 5 comments
        response = requests.get(
            f"https://oauth.reddit.com/r/{subreddit}/hot?limit=5", headers=headers)

        response.raise_for_status()
        post = get_postFromJson(response.json())

        posts.append(post)

    return posts


def get_postFromJson(jsonResponse):

    listOfPost = []
    for post in jsonResponse['data']['children']:
        dictionary = {}

        if post['data']['stickied']:
            print('skipping pinned post usually by mods')
        else:
            # Add only posts with text
            if post['data']['selftext']:
                dictionary[post['data']['title']] = post['data']['selftext']

            # check for post with media
            if (is_key_present(post['data'], 'post_hint') and is_key_present(post['data'], 'url_overridden_by_dest')):
                if post['data']['post_hint'] == 'image' or post['data']['post_hint'] == 'video':
                    dictionary[post['data']['title']
                               ] = post['data']['url_overridden_by_dest']
                elif post['data']['url_overridden_by_dest']:
                    dictionary[post['data']['title']
                               ] = post['data']['url_overridden_by_dest']

            listOfPost.append(dictionary)

    return listOfPost
