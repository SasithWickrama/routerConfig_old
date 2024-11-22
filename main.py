import paramiko
import time
import config
 

if __name__ == '__main__':


    # Create instance of SSHClient object
    remote_conn_pre = paramiko.SSHClient()

    # Automatically add untrusted hosts (make sure okay for security
    # policy in your environment)
    remote_conn_pre.set_missing_host_key_policy(
         paramiko.AutoAddPolicy()
    )

    # initiate SSH connection
    remote_conn_pre.connect(
        config.HOST, 
        username=config.USER, 
        password=config.PASSWD, 
        look_for_keys=False, 
        allow_agent=False
    )
    print ("SSH connection established to %s" % config.HOST)
    
    
    # Use invoke_shell to establish an 'interactive session'
    remote_conn = remote_conn_pre.invoke_shell()
    print ("Interactive SSH session established")


    # Now let's try to send the router a command
    remote_conn.send("display current-configuration interface GigabitEthernet 1/0/4 \n")

    # Wait for the command to complete
    time.sleep(2)
    
    output = remote_conn.recv(1000)
    #output = ssh_stdout.readlines()
    print(output.decode("utf-8") )
    
    text_file = open("sample.txt", "w")
    text_file.write(output.decode("utf-8"))
    text_file.close()
    
    
    with open("sample.txt", "r") as f:
        for line in f.readlines():
            if 'description' in line:
                #str1= line
                print(line.split(" ")[3].split("_")[0])
            if 'user-queue' in line:
                if 'inbound' in line:
                
                    print("CIR IN"+line.split(" ")[3])
                    print("PIR IN"+line.split(" ")[5])
                if 'outbound' in line:
                #str2= line
                    print("CIR "+line.split(" ")[3])
                    print("PIR "+line.split(" ")[5])                  



        
            
            
            