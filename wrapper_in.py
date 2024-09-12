import argparse
import os
import time
import subprocess

parser = argparse.ArgumentParser(description='Specify URL and EXTN for wrapper_in.py')
parser.add_argument('--url', type=str)
parser.add_argument('--extn', type=str)
args = parser.parse_args()

os.chdir('./accads_crawler')

start_time = time.time()

cmd = f'npm run crawl -- -u {args.url} -o /{args.extn}/ -v -f -d "requests,cookies,ads,screenshots,cmps,videos" --reporters "cli,file" -l /{args.extn}/ --autoconsent-action "optIn" --extn {args.extn}'

process = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

while True:
    curr_time = time.time()
    if curr_time - start_time < 220 and process.poll() is None: # process.poll() in None if the process is still running
        time.sleep(5)
    else:
        print(f"Process for {args.url} is still running. Terminating it.")
        process.terminate()  # Gracefully terminate the process
        time.sleep(2)
        if process.poll() is None:
            process.kill() # Forceful termination
        break
