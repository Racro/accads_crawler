import subprocess
import multiprocessing
import os
import time

# List of URLs to be crawled
urls = open('websites.txt', 'r').read().splitlines()

# Docker container names
containers = ["accads_control", "accads_adblock"]
# containers = ["accads_control"]

# Build Docker images (assuming Dockerfiles are in the current directory)
subprocess.run(["docker", "build", "-t", "accads", "-f", "Dockerfile", "."])

# Function to create a directory with 777 permission
def create_directory(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        os.chmod(dir_name, 0o777)
        print(f"Created {dir_name} with 777 permissions.")
    else:
        print(f"{dir_name} already exists.")

def create_data_directories():
    # Directories to be created
    dir1 = "./control"
    dir2 = "./adblock"

    # Create both directories
    create_directory(dir1)
    create_directory(dir2)

def check_and_start_container(container_name, image_name, extn):
    """Check if a container is running and start it if it's not."""
    result = subprocess.run(["docker", "ps", "-q", "-f", f"name={container_name}"], capture_output=True, text=True)
    if not result.stdout.strip():
        print(f"Starting container: {container_name}")
        subprocess.run(["docker", "run", "-d", "--name", container_name, "-v", f"./{extn}:/{extn}", image_name])
    else:
        print(f"Container {container_name} is already running.")

def feed_url_to_container(container_name, url, extn):
    command = f'docker exec -i {container_name} python3 wrapper_in.py --url={url} --extn={extn}'
    os.system(command)

def handle_container(container_name, image_name, url, extn):
    check_and_start_container(container_name, image_name, extn)
    feed_url_to_container(container_name, url, extn)
    time.sleep(1)  # Add delay if necessary

create_data_directories()
for url in urls:
    # Create multiprocessing processes
    processes = []
    image_name = "accads"
    p1 = multiprocessing.Process(target=handle_container, args=(containers[0], image_name, url, 'control'))
    p2 = multiprocessing.Process(target=handle_container, args=(containers[1], image_name, url, 'adblock'))
    
    p1.start()
    p2.start()

    TIMEOUT = 70
    start = time.time()
    print("joining jobs")
    # Wait for all processes to finish
    p1.join(timeout = 60)
    p2.join(timeout = 60)

    while time.time() - start <= TIMEOUT:
        if p1.is_alive():
            p1.terminate()
        if p2.is_alive():
            p2.terminate()

    time.sleep(2)

# Optionally, stop and remove containers after use
# for container in containers:
#     subprocess.run(["docker", "stop", container])
    # subprocess.run(["docker", "rm", container])

