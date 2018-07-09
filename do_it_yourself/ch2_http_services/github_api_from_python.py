import requests
import json


def main():

    user, repo = get_repo_info()

    # url = 'https://api.github.com/repos/mikeckennedy/consuming_services_python_demos'
    url = 'https://api.github.com/repos/{}/{}'.format(user, repo)
    response = requests.get(url)

    if response.status_code != 200:
        print("Error accessing repo: {}".format(response.status_code))
        return

    repo_data = response.json()
    print()
    print("To clone {}'s repo named {}".format(user, repo))
    print("The command is: ")
    print()
    print("git clone {}".format(repo_data.get('clone_url', 'ERROR: no clone URL')))


def get_repo_info():

    user = input("What is the username? ")
    repo = input("What is the repo name? ")

    return user, repo


if __name__ == '__main__':
    main()