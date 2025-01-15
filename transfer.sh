#!/bin/bash
# Save this as transfer.sh in your local machine

# Transfer Python files
scp python_src/*.py pi@192.168.68.80:~/work/python_src/

# Transfer HTML and other files
scp *.html *.sh pi@192.168.68.80:~/work/

# Restart the service
ssh pi@192.168.68.80 "sudo systemctl restart xr_robot" 