import argparse
import os
import time
import subprocess

parser = argparse.ArgumentParser(description='Specify URL and EXTN for wrapper_in.py')
parser.add_argument('--url', type=str)
parser.add_argument('--extn', type=str)
args = parser.parse_args()

os.chdir('./accads_crawler')

# start_time = time.time()

cmd = f'npm run crawl -- -u {args.url} -o /{args.extn}/ -v -f -d "requests,cookies,ads,screenshots,cmps,videos" --reporters "cli,file" -l /{args.extn}/ --autoconsent-action "optIn" --extn {args.extn}'
# cmd = [
#         'npm', 'run', 'crawl', '--',
#         '-u', args.url,
#         '-o', f'/{args.extn}/',
#         '-v', '-f', '-d', 'requests,cookies,ads,screenshots,cmps,videos',
#         '--reporters', 'cli,file',
#         '-l', f'/{args.extn}/',
#         '--autoconsent-action', 'optIn',
#         '--extn', args.extn
#     ]
# process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
os.system(cmd)