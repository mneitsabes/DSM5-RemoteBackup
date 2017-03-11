#!/usr/bin/python2
import sys
import commands
import json
import re
from os import listdir
from os.path import isfile, join
from os import environ

class BackupLog(object):
	'''
	Represent all informations about a backup log :
		- Begin time
		- End time
		- Return code
		- Amount of data sent
		- Amount of data received
		- Average speed
		- Amount of files impacted 
		- Remote backup size
	'''

	def __init__(self, beginTime=None, endTime=None, rc=None, dataSent=None, dataReceived=None, avgSpeed=None, nbFilesImpacted=None, remoteBackupSize=None, row=None):
		'''
		Initialize with all informations throught parameters or with "row"
		'''
		if row == None:	
			self.beginTime = beginTime
			self.endTime = endTime
			self.rc = rc
			self.dataSent = dataSent
			self.dataReceived = dataReceived
			self.avgSpeed = avgSpeed
			self.nbFilesImpacted = nbFilesImpacted
			self.remoteBackupSize = remoteBackupSize
		else:
			self.beginTime = row[0]
			self.endTime = row[1]
			self.rc = row[2]
			self.dataSent = row[3]
			self.dataReceived = row[4]
			self.avgSpeed = row[5]
			self.nbFilesImpacted = row[6]
			self.remoteBackupSize = row[7]

	def getBeginTime(self):
		'''
		Retrieve begin time
		'''
		return self.beginTime

	def getRC(self):
		'''
		Retrieve return code
		'''
		return self.rc

	def getDataSent(self):
		'''
		Retrieve amount of data sent
		'''
		return self.dataSent

	def getDataReceived(self):
		'''
		Retrieve amount of data received
		'''
		return self.dataReceived
		
	def getAvgSpeed(self):
		'''
		Retrieve average speed
		'''
		return self.avgSpeed

	def getNbFilesImpacted(self):
		'''
		Retrieve amount of files impacted
		'''
		return self.nbFilesImpacted

	def getRemoteBackupSize(self):
		'''
		Retrieve remote backup size
		'''
		return self.remoteBackupSize
		
	def toJSON(self):
		'''
		Output this object as JSON string
		'''
		str = "{"
		str += "\"beginTime\": \"%s\", " % self.beginTime
		str += "\"endTime\": \"%s\", " % self.endTime
		str += "\"rc\": \"%s\", " % self.rc
		str += "\"dataSent\": \"%s\", " % self.dataSent
		str += "\"dataReceived\": \"%s\", " % self.dataReceived
		str += "\"avgSpeed\": \"%s\", " % self.avgSpeed
		str += "\"nbFilesImpacted\": \"%s\", " % self.nbFilesImpacted
		str += "\"remoteBackupSize\": \"%s\"" % self.remoteBackupSize
		str += "}"
		return str

class BackupLogList(list):
	'''
	List of backup logs with JSON output
	'''
	def toJSON(self):
		'''
		Output this object as JSON string
		'''
		str = "["
		
		first = True
		for backupLogObj in self:
			if first:
				first=False
			else:
				str += ","
				
			str += backupLogObj.toJSON()
			
		str += "]"
		return str

class BackupLogManager(object):
	'''
	Manager backup logs
	'''
	
	def __init__(self):
		'''
		Construct the manager
		'''
		self.directoryLogPath = "/volume1/@appstore/remotebackup/logs"

	def getLatestLog(self):
		'''
		Get the lastest available log file
		'''
		fp = open("%s/latest.info" % self.directoryLogPath, "r")
		logContent = fp.read()
		fp.close()
		
		return self.transformLogToObj(logContent)
		
	def getAllLogs(self):
		'''
		Retrieve all logs
		'''
		# Retrieve all files in <self.directoryLogPath>/*.info except lastest.info
		filesLogInfo = [ f for f in listdir(self.directoryLogPath) if isfile(join(self.directoryLogPath, f)) and f.endswith(".info") ]
		filesLogInfo.remove("latest.info")
		
		# Sort by date (recent the top, oldest on the bottom
		filesLogInfo.sort(reverse=True)
		
		# Transform logfile to object
		backupLogObjects = BackupLogList()
		
		# For each logfile
		for file in filesLogInfo:
			fp = open("%s/%s" % (self.directoryLogPath, file), "r")
			logContent = fp.read()
			fp.close()
		
			# Create the object and add it to the list
			backupLogObjects.append(self.transformLogToObj(logContent))
		
		return backupLogObjects

	def transformLogToObj(self, logContent):
		'''
		Transform a log content to a BackupLog object
		
		A transform log is a text file wich contains KEY=VALUE pair :
			BEGIN=<date and time when the backup began formatted like DD/MM/YYYY HH:MM:SS>
			END=<date and time when the backup ended formatted like DD/MM/YYYY HH:MM:SS>
			RC=<return code of rsync : 0 means succesfull backup, >0 means that an error occured>
			TRANSFERT_DATA_SENT=<size of sent data : XX.XX{K|M|G}>
			TRANSFERT_DATA_RECEIVED=<size of received data : XX.XX{K|M|G}>
			TRANSFERT_SPEED=<average speed of the backup XX.XX{K|M|G}>
			TRANSFERT_NB_FILES_IMPACTED=<number of files impacted by this backup^>
			REMOTE_BACKUP_SIZE=<size of the backup on the destination XX.XX{K|M|G}> 
		'''
		# Used to create the object from the collection
		objectInitRow = []
		
		# Dictonary KEY:POSITION_IN_COLLECTION
		refRowId = { "BEGIN": 0, "END": 1, "RC": 2, "TRANSFERT_DATA_SENT": 3, "TRANSFERT_DATA_RECEIVED": 4, "TRANSFERT_SPEED": 5, "TRANSFERT_NB_FILES_IMPACTED": 6, "REMOTE_BACKUP_SIZE": 7 }
		
		# Read line by line
		lines = logContent.splitlines()
		for line in lines:
			# Separe key from value
			key,value = line.split("=")
		
			# If the key exists...
			if key in refRowId:
				# Retrieve the position in the collection by refRowId[key] and insert the value at this position
				objectInitRow.insert(refRowId[key], value)	
	
		return BackupLog(row=objectInitRow)

def getSynoToken():
	'''
	Get the SYNO token (used to prevent CRSF attacks)
	'''
	# Get the token (JSON format)
	loginOutput = commands.getoutput("/usr/syno/synoman/webman/login.cgi") 
	
	# Select only the JSON datas (not the HTTP response header like Content-type...)
	m = re.search("\{(.*)\}", loginOutput, re.DOTALL|re.MULTILINE)
	
	if m is None: # If no JSON found
		return False
	else:
		json_input = m.group(0)

		try:
			decoded = json.loads(json_input) # Decoe JSON
			
			# When the user is not logged, the resposne is { "reason" : "error_cantlogin", "result" : "error", "success" : false }
			# When the use is logged, the response is { "SynoToken" : "wVSzKRmjn663s", "result" : "success", "success" : true }
			if decoded['result'] == "error":
				return False
			else:
				return decoded['SynoToken']
		except (ValueError, KeyError, TypeError):
			return False

def isUserLogged():
	'''
	Determine if the user is authentified
	'''
	return True if getSynoToken() is not False else False

def getHttpGetParams():
	'''
	Retrieve the HTTP GET parameters of the scrip
	'''
	httpGetParams = {}
	
	if "REQUEST_URI" in environ: # script executed through the webman
		# environ['REQUEST_URI'] contains the full URI, e.g: /webman/3rdparty/RemoteBackup/test.cgi?op=x&y=z&blabla
		# environ['SCRIPT_NAME'] contains the script path, e.g: /webman/3rdparty/RemoteBackup/test.cgi
		# we need to remove environ['SCRIPT_NAME'] followed by the character "?" to have the part that contains only parameters
		paramStr = environ['REQUEST_URI'].replace("%s?" % environ['SCRIPT_NAME'], "")
		
		# Split the parameter by the separator "&"
		paramGroups = paramStr.split("&")
		
		# For each group, try to find a key=value pair
		for paramGroup in paramGroups:
			try:
				key,value = paramGroup.split("=")
				httpGetParams[key] = value
			except: # if not properly structured, skip
				pass
	elif "SHELL" in environ: # script executed in a shell
		pass
	else: # other not supported
		raise
		
	return httpGetParams

def getHttpGetParam(key):
	'''
	Get the GET parameter pointed by key
	'''
	httpGetParams = getHttpGetParams()
	
	value = None
	try: 
		value = httpGetParams[key]
	except:
		pass
		
	return value

# Main entry point
if __name__ == '__main__':
	# Acces is reserved for logged  user only
	#if not isUserLogged():
	#	exit(1)
	
	# HTTP Response
	sys.stdout.write("Content-type: text/html; charset=utf-8\r\n")
	sys.stdout.write("\r\n")

	## !!!!!!!!! TODO satanize input

	# Get (if provided) the GET parameter named
	op = getHttpGetParam("op")

	# Initialize the backup manager
	backupLogManager = BackupLogManager()

	# Controller "switch"
	if op == "log_getlatest":
		latestLog = backupLogManager.getLatestLog()
		print(latestLog.toJSON())
	elif op == "log_getall":
		allLogs = backupLogManager.getAllLogs()
		print(allLogs.toJSON())