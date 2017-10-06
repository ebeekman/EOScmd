#!/usr/bin/python

import sys
import getopt
import json
import requests
import getpass

class HandleConfiguration:
    switch_name = None
    switch_cmd = None

    def getarguments(self):
        try:
           opts, args = getopt.getopt(sys.argv[1:], "H:c:p:u:",["host=","cmd=","port=","user="])
        except getopt.GetoptError:
           print 'EOS_runcmd.py -H <host> -c <command> -p <API port> -u <None/username'
           sys.exit(2)
        for opt, arg in opts:
           if opt in ("-H", "--host"):
              # Hostname
              self.switch_name = arg
           elif opt in ("-c", "--cmd"):
              # command
              self.switch_cmd = arg
           elif opt in ("-p", "--port"):
              # API port 
              self.switch_port = arg
           elif opt in ("-u", "--user"):
              # user 
              if arg == "None":
                 self.switch_username = ""
                 self.switch_password = "" 
              else:
                 self.switch_username = arg 
                 self.switch_password = getpass.getpass("Password:")

    def executecommand(self):
       switches = [self.switch_name]
       cmd = [self.switch_cmd]

       for switch in switches:
          urlString = "http://%s:%s/command-api" % (switch, self.switch_port)
          switchReq = requests.session()
          switchReq.auth = (self.switch_username,self.switch_password)
          switchReq.verify = False
          switchReq.headers.update({'Content-Type' : 'application/json'})

          data = {'jsonrpc': '2.0','method': 'runCmds','params': {'format': 'json','timestamps': False,'cmds': [''], 'version': 1}, 'id': 'PythonScript-1'}

          data['params']['cmds'] = cmd 
          response = switchReq.request('post', urlString, data=json.dumps(data))
          print json.dumps(response.json(), indent=2)

if __name__ == "__main__":
    # First build up the config via the arguments and the config file
    config = HandleConfiguration()
    config.getarguments()
    config.executecommand()
