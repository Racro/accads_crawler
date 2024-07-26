import argparse
import os

parser = argparse.ArgumentParser(description='start add collection')
parser.add_argument('--url', type=str)
parser.add_argument('--extn', type=str)
args = parser.parse_args()

os.chdir('./accads_crawler')

os.system(f'npm run crawl -- -u {args.url} -o /{args.extn}/ -v -f -d "requests,cookies,ads,screenshots,videos" --reporters "cli,file" -l /{args.extn}/ --autoconsent-action "optIn" --extn {args.extn}')