import os
import sys
import requests
import argparse
import appdirs

try:
    import magic
    HAS_MAGIC = True
except Exception:
    HAS_MAGIC = False


APP_NAME = 'teleput_cli'
SERVER = 'https://teleput.textual.ru'


def read_key() -> str:
    filename = os.path.join(appdirs.user_config_dir(APP_NAME), 'key')
    if not os.path.exists(filename):
        return None
    with open(filename, 'r') as f:
        return f.read().strip()


def write_key(key: str):
    filename = os.path.join(appdirs.user_config_dir(APP_NAME), 'key')
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    with open(filename, 'w') as f:
        f.write(key)


def mime_from_filename(name: str) -> str:
    _, ext = os.path.splitext(name)
    if ext == '.png':
        return 'image/png'
    elif ext in ('.jpg', '.jpeg'):
        return 'image/jpeg'
    elif ext == '.gif':
        return 'image/gif'
    elif ext in ('.mp4', '.mpeg4'):
        return 'video/mp4'
    elif ext == '.mp3':
        return 'audio/mpeg'
    elif ext == '.m4a':
        return 'audio/m4a'
    elif ext == '.ogg':
        return 'audio/ogg'
    else:
        return None


def main():
    parser = argparse.ArgumentParser(
        description='Send text and files to the Teleput Telegram Bot.')
    parser.add_argument('-k', '--key', help='Set or update your Teleput key')
    parser.add_argument('-r', '--raw', action='store_true',
                        help='Send the file without compression')
    parser.add_argument('what', nargs='*',
                        help='Text or a file name to send. Add second argument for a description')
    options = parser.parse_args()

    if options.key:
        key = options.key
        write_key(key)
    else:
        key = read_key()
    if not key:
        print('Please run this tool with -k <your_key> argument.')
        print('To get your key, open https://t.me/teleput_bot and click "Start".')
        sys.exit(3)

    if not options.what:
        if options.key:
            print('Saved the new key.')
            sys.exit(0)
        else:
            print('Please specify what do you want to send.')
            sys.exit(1)

    if os.path.exists(options.what[0]):
        fields = {'key': key}
        if options.raw:
            fields['raw'] = 1
        if len(options.what) >= 2:
            if options.what[-1] == '-':
                fields['text'] = sys.stdin.read()
            else:
                fields['text'] = options.what[-1]
        if HAS_MAGIC:
            mime_type = magic.from_file(options.what[0], mime=True)
        else:
            mime_type = mime_from_filename(options.what[0])
        files = {
            'media': (
                options.what[0],
                open(options.what[0], 'rb'),
                mime_type,
            )
        }
        resp = requests.post(SERVER + '/upload', fields, files=files)
        if resp.status_code != 200:
            print(f'Error: {resp.text}')
            sys.exit(4)
    else:
        if options.what[0] == '-':
            text = sys.stdin.read()
        else:
            text = options.what[0]
        fields = {
            'key': key,
            'text': text,
        }
        resp = requests.post(SERVER + '/post', fields)
        if resp.status_code != 200:
            print(f'Error {resp.status_code}: {resp.text}')
            sys.exit(4)
