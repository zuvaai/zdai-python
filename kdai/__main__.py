from .config import config
from .KDAISDK import KDAISDK
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--get",
                    type = str,
                    choices = ["url", "token"],
                    help = 'Returns the default url used by the wrapper')
parser.add_argument("--set-token",
                    type = str,
                    help = 'Sets the default token')
parser.add_argument("--set-url",
                    type = str,
                    help = 'Sets the default url')
parser.add_argument("--test",
                    type = str,
                    choices = ["connection"],
                    help = 'Perform an test action')

args = parser.parse_args()

if __name__ == "__main__":
    config.create_wrapper_config()
    url, token = config.get_access()

    if args.get == "token":
        if not token:
            print(f'No default token found')
        else:
            print(token)
    elif args.get == "url":
        if not url:
            print(f'No default url found')
        else:
            print(url)
    elif args.set_token:
        config.update_wrapper_config(token = args.set_token)
        print('Token set')
    elif args.set_url:
        config.update_wrapper_config(url = args.set_url)
        print('Url set')
    elif args.test == 'connection':
        if any(f == "" for f in [url, token]):
            print(f'Unable to perform connection test using default values: either url or token missing.')
            exit(1)

        sdk = KDAISDK(from_config = True)

        try:
            fields, _ = sdk.fields.get()
            print(f'Connection test succeeded [Retrieved {len(fields)} fields]')
        except Exception as e:
            print(f'Connection test failed: {e}')
