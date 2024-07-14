import subprocess
import os
import time
from colorama import init, Fore

init(autoreset=False)

red = Fore.RED
green = Fore.GREEN
yellow = Fore.YELLOW
blue = Fore.BLUE

os.system("cls")
print(f"""{red}
 _____                 _            _____ _               _             
/  ___|               (_)          /  __ \ |             | |            
\ `--.  ___ _ ____   ___  ___ ___  | /  \/ |__   ___  ___| | _____ _ __ 
 `--. \/ _ \ '__\ \ / / |/ __/ _ \ | |   | '_ \ / _ \/ __| |/ / _ \ '__|
/\__/ /  __/ |   \ V /| | (_|  __/ | \__/\ | | |  __/ (__|   <  __/ |   
\____/ \___|_|    \_/ |_|\___\___|  \____/_| |_|\___|\___|_|\_\___|_|   
      """)

def check_service_status(service_name):
    try:
        output = subprocess.check_output(["sc", "query", service_name], stderr=subprocess.STDOUT, universal_newlines=True)
        return "RUNNING" in output
    except subprocess.CalledProcessError:
        return False

def start_service(service_name):
    try:
        subprocess.check_output(["sc", "start", service_name], stderr=subprocess.STDOUT, universal_newlines=True)
        print(f"\n{blue}[{green}+{blue}] {green}Service {yellow}{service_name} {green}started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"{blue}[{red}ERROR{blue}] {red}Error in starting the service {service_name}: {e.output}")

services = ["dps", "spooler", "bam", "sysmain", "pcasvc"]

all_running = True

for service in services:
    if check_service_status(service):
        print(f"{blue}[{green}!{blue}] {green}Service {yellow}{service} {green}is running.")
    else:
        print(f"{blue}[{red}!!{blue}] {red}Service {yellow}{service} {red}is not running.")
        all_running = False
        start = input(f"{blue}[{red}!!{blue}] {yellow}Do you wish to start the service {service}? ({green}s{yellow}/{red}n{yellow}): ").lower()
        if start == 's':
            start_service(service)
            time.sleep(1)
            if check_service_status(service):
                print(f"{blue}[{green}!{blue}] {green}Service {yellow}{service} {green}is now running.")
            else:
                print(f"{blue}[{red}!!{blue}] {red}Service {yellow}{service} {red}failed to start.")
        else:
            print(f"{blue}[{red}!!{blue}] {red}Service {service} will not be started.\n")

if all_running:
    print(f"{blue}[{green}!{blue}] {green}All processes are currently running.")
else:
    print(f"{blue}[{red}-{blue}] {red}Not all processes are running.")

input(f"\n{yellow}Press enter to close the program.")
os._exit(0)
