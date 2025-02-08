# import subprocess

# # Path to the text file containing file names
# file_names_path = "C:/Sukhendu/UPWORK-WORK/PIERRE-Data_Engineer/DUMPS_Files/allFileNames.txt"

# # Path to save the files locally
# local_path = "C:/Sukhendu/UPWORK-WORK/PIERRE-Data_Engineer/DUMPS_Files/allCsv/"

# # SSH command details
# ssh_user = "18108643"
# ssh_host = "jcyared-04-02-2024-18108643.dev.odoo.com"
# remote_dir = "Table-Csv"

# # Read file names from the .txt file
# with open(file_names_path, 'r', encoding='utf-16 le') as file:
#     for line in file.readlines():
#         # Get the file name (remove any leading/trailing whitespace)
#         file_name = line.strip()

#         if file_name:
#             # Construct the SSH command
#             ssh_command = f"plink.exe -l {ssh_user} -pw Sohan#2011 {ssh_host} /"cat {remote_dir}/{file_name}/""
 
#             # Construct the local file path
#             local_file_path = f"{local_path}{file_name}"

#             # Use plink to execute the SSH command
#             cmd = f"plink.exe -l {ssh_user} -pw Sohan#2011 {ssh_host} /"cat {remote_dir}/{file_name}/" > {local_file_path}"

#             #print(Cmd)
#             #continue

#             # Execute the SSH command and redirect output to the local file
#             try:
#                 subprocess.run(cmd, shell=True, check=True)
#                 print(f"Processed {file_name}")
#             except subprocess.CalledProcessError as e:
#                 print(f"Error processing {file_name}: {e}")



######   OLD CODE   

import subprocess
#import wexpect

# Path to the text file containing file names
file_names_path = "D:/Sohan Sain/Programming/Project&Jobs/PierreDataCreate/allFileNames.txt"

# Path to save the files locally
local_path = "D:/Sohan Sain/Programming/Project&Jobs/PierreDataCreate/allTxt/"

# SSH command details
ssh_user = "18108643"
ssh_host = "jcyared-04-02-2024-18108643.dev.odoo.com"
remote_dir = "Table-Defs"

# Read file names from the .txt file
with open(file_names_path, 'r') as file:
    for line in file.readlines():
        # Get the file name (remove any leading/trailing whitespace)
        file_name = line.strip()

        if file_name:
            # Construct the SSH command
            ssh_command = f"ssh {ssh_user}@{ssh_host} \"cat ./{remote_dir}/{file_name}\""

            # Construct the local file path
            local_file_path = f"{local_path}{file_name}"
            # Use sshpass to automatically provide the password
            cmd = f"{ssh_command} > \"{local_file_path}\""

            #print(Cmd)
            #continue

            # Execute the SSH command and redirect output to the local file
            try:
                subprocess.run(cmd, shell=True, check=True)
                # print(cmd)
                # child = wexpect.spawn(cmd) 
                # child.expect("Enter passphrase for key 'C://Users//s_sai/.ssh/id_rsa': ") 
                # child.sendline('Sohan#2011') 
                # process = subprocess.Popen([cmd], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                # process.stdin.write('Sohan#2011/n')
                # process.stdin.flush()
                # output, error = process.communicate()#input="Sohan#2011/n")
                # print(output, error)
                print(f"Processed {file_name}")
            except subprocess.CalledProcessError as e:
                print(f"Error processing {file_name}: {e}")