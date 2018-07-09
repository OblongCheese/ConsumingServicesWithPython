import shutil
import requests
import os
import math
from xml.etree import ElementTree


def main():
    mp3_files = get_episode_files('https://talkpython.fm/rss')
    for file in mp3_files[:3]:
        download_file(file, "C:\\Users\\ostickle\\Music")


def get_episode_files(url):
    resp = requests.get(url)
    xml_text = resp.text

    dom = ElementTree.fromstring(xml_text)

    return [
        enclosure_node.attrib['url']
        for enclosure_node in dom.findall('channel/item/enclosure')
    ]


def download_file(file, dest_folder):
    # stream and decode the inbound binary data stream
    # why?
    # this initiates an http request to retrieve the content length (size of file)
    resp_size = requests.get(file, stream=True).headers['Content-Length']
    # this initiates the second http request to download the file
    resp = requests.get(file, stream=True)
    resp.decode_content = True

    base_file = os.path.basename(file)
    dest_file = os.path.join(
        os.path.abspath(dest_folder), base_file
    )
    print("Downloading and saving " + base_file + " which is {}Mb.".format(
        (str(math.ceil(int(resp_size) / 1024 / 1024))
        )))

    # create a file stream that is writable and binary
    # use the shutil to copy binary data from one stream to another stream
    with open(dest_file, 'wb') as fout:
        # the next line will run until the file download has been completed
        shutil.copyfileobj(resp.raw, fout)
        # TODO: implement a progress bar or percentage readout
        # https://stackoverflow.com/questions/29967487/get-progress-back-from-shutil-file-copy-thread
        #statinfo = os.stat(dest_file)
        #percent = (statinfo.st_size / resp_size) * 100
        #print(">>> Progress: {}%".format(math.ceil(percent)), end='\r', flush=True)


if __name__ == '__main__':
    main()