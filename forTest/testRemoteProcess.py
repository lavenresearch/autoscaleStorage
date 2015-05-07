from remoteProcess import remoteProcess

remoteAS = remoteProcess("a.py", "192.168.3.121")
remoteAS.getPID()
a = raw_input("type:")
remoteAS.killProcess()

