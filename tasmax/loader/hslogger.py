#
# Simple looger for loader
#
log_level = "INFO"

def debug(msg):
	if log_level == "DEBUG":
		print("DEBUG> " + msg)
	 

def info(msg):
	if log_level not in  ("ERROR", "WARNING", "WARN"):  
		print("INFO> " + msg)
	 

def warn(msg):
	if log_level != "ERROR":
		print("WARN> " + msg)
	 

def warning(msg):
	if log_level != "ERROR":
		print("WARN> " + msg)
	 
def error(msg):
	print("ERROR> " + msg)
	 


 