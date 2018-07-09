import requests


def main():
    url = 'https://talkpython.fm'
    try:
        response = requests.get(url)

        if response.status_code != 200:
            print("Error {} requesting the URL.".format(response.status_code))
            return

        print(response.text[:500])

    except Exception as e:
        print("There was some kind of problem with the request.")
        print("Exception: {}".format(type(e)))


if __name__ == '__main__':
    main()