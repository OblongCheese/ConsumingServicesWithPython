import datetime
import json
import requests
import collections

Post = collections.namedtuple("Post", 'id title content published view_count')

base_url = 'http://consumer_services_api.talkpython.fm/'


def show_posts(posts):
    if not posts:
        print("Sorry, no posts to show.")
        return

    print("---------------------------- BLOG POSTS ----------------------------")
    max_width = max((len('{:,}'.format(int(p.view_count))) for p in posts))
    for idx, p in enumerate(posts):
        padded = ' ' * (max_width - len('{:,}'.format(int(p.view_count))))
        print("{}. {} [{}{:,}]: {}".format(idx + 1, p.id, padded, int(p.view_count), p.title))
    print()


def get_posts():
    url = base_url + 'api/blog/'
    headers = {'Accept': 'application/json'}
    response = requests.get(url, headers)

    if response.status_code != 200:
        print("Error downloading posts: {} {}".format(response.status_code, response.text))
        return []

    return [
        Post(**post)
        for post in response.json()
    ]


def add_post():
    now = datetime.datetime.now()
    published_text = '{}-{}-{}'.format(now.year, str(now.month).zfill(2), str(now.day).zfill(2))

    title = input("Title: ")
    content = input("Content: ")
    view_count = int(input("View count: "))

    post_data = dict(title=title, content=content, view_count=view_count, published_text=published_text)
    url = base_url + 'api/blog/'
    headers = {'Content-type': 'application/json'}

    response = requests.post(url, json=post_data, headers=headers)
    if response.status_code != 201:
        print("Error creating post: {} {}".format(response.status_code, response.text))

    post_response = response.json()
    print("Created this: ")
    print(post_response)


def update_post():
    print("To update a post, please choose the post from the list below: ")
    posts = get_posts()
    show_posts(posts)
    print()

    # remember that we start numbering from zero
    posts = posts[int(input('Number: '))-1]

    print('Leave any field blank to retain the existing information.')
    # display the new title prompt with the old title written in square brackets
    title = input('Title: ['+post.title+'] ')
    # accept the new title, or if blank, use the old title
    title = title if title else post.title

    content = input('Content: ['+post.content+'] ')
    content = content if content else post.content

    view_count = input('View count: ['+str(view_count)+'] ')
    view_count = view_count if view_count else post.view_count

    post_data = dict(title=title, content=content, view_count=view_count, published=post.published)

    url = base_url + 'api/blog/' + post.id
    response = requests.put(url, data=json.dumps(post_data))

    if response.status_code != 204:
        print("There was an error updating this post: {} {}".format(response.status_code, response.text))

    print("Successfully updated '{}'".format(post.title))


def delete_post():
    print("To delete a post, please choose the post from the list below: ")
    posts = get_posts()
    show_posts(posts)
    print()

    post = posts[int(input('The number of the post to delete: '))-1]

    print("Deleteing {} ...".format(post.title))

    url = base_url + 'api/blog/' + post.id
    response = requests.delete(url)

    if response.status_code != 202:
        print("There was an error deleting this post: {} {}".format(response.status_code, response.text))

    print("Deletion of '{}' is complete.".format(post.title))


def main():
    while True:
        action = input("What would you like to do with the blog API? \r\n"
                       "[l]ist, [a]dd, [u]pdate, [d]elete, e[x]it: ")
        if action == 'x':
            print('Exiting...')
            break
        if action == 'l':
            posts = get_posts()
            show_posts(posts)
        if action == 'a':
            add_post()
        if action == 'u':
            update_post()
        if action == 'd':
            delete_post()
        else:
            print("Please enter a valid response.")


if __name__ == '__main__':
    main()