
from logging import getLogger, INFO
from cloghandler import ConcurrentRotatingFileHandler
import multiprocessing,subprocess
import os,time

class RSH_RUNNER:
	__runner_requestor__        =    ''
	__operating_machine__       =    ''
	__log_path__                =    ''
	__parellel_exec__           =    false
	__parellel_proc__           =    0
	__command_queue__           =    []
	__log_id__                  =    ''
	__return_content__          =    ''
	

	self.__init__(self,requestor,machine,log_path,parellel_proc,command_queue):
		self.__runner_requestor__        =    requestor
		self.__operating_machine__       =    machine
		self.__log_path__                =    log_path
		self.__parellel_proc__           =    parellel_proc
		sefl.__command_queue__           =    command_queue

	def __run__(self):
		"""
		func __run__ is the wrapper for the real run
		"""
		pidlet  = []
		lock    = multiprocessing.Lock()
		for cmd in self.__command_queue__:
			process = multiprocessing.Process(target=__cmd__,args=(lock,cmd))
			process.start()
			pidlet.append(process)
		
		for p in pidlet:
			p.join()
		
		return self.__return_content__


	def __cmd__(self,lock,command):

		log = getLogger()

		# buid log path
		sefl.__log_id__    =  self.__runner_requestor__+'_'+time.strftime("%Y_%H_%M_%S")+'.log'
		logfile            =  os.path.join(log_path,self.__log_id__)

		# Rotate log after reaching 10M, keep 5 old copies.
		rotateHandler = ConcurrentRotatingFileHandler(logfile, "a", 1024*1024*10, 5)
		log.addHandler(rotateHandler)


		p=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE) 
		(stdout,errout)    =  p.communicate()
		if stdout:
			lock.acquire()
			self.__return_content__    =+  command + ':' + stdout
			lock.release()
			log.setLevel(INFO)
			log.info(time.strftime("%b %d %Y %H:%M:%S:  ")+command+':'+stdout)
		if errout:
			lock.acquire()
			self.__return_content__    =+  command + ':' + errout
			lock.release()
			log.setLevel(ERROR)
			log.info(time.strftime("%b %d %Y %H:%M:%S:  ")+command+':'+errout)
		





