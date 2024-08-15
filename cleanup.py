import os

os.system('docker stop accads_control accads_adblock')
os.system('docker rm accads_control accads_adblock')

os.system('docker image rm accads')
os.system('docker buildx prune')
os.system('docker build -t accads -f Dockerfile .')

os.system('docker run -d -it --name accads_control -v ./control:/control accads')
os.system('docker run -d -it --name accads_adblock -v ./adblock:/adblock accads')
