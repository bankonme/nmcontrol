import plugin

class pluginMain(plugin.PluginThread):
	name = 'main'
	options = {
		'start':	['Launch at startup', 1],
		'debug':	['Debug mode', 0, '<0|1>'],
		'daemon':	['Background mode', 1, '<0|1>'], 
		#'plugins':	['auto started plugins', 'main,data,rpc'],
	}

	def pStatus(self):
		ret = ''
		if self.running:
			ret = "Plugin " + self.name + " running"
		for plugin in self.app['plugins']:
			if plugin != 'main' and self.app['plugins'][plugin].running:
				ret += '\n' + self.app['plugins'][plugin].pStatus()

		return ret

	def pStop(self):
		if self.app['debug']: print "Plugin %s stopping" %(self.name)
		self.running = False
		for plugin in self.app['plugins']:
			if self.app['plugins'][plugin].running == True:
				self.app['plugins'][plugin].stop()
		print "Plugin %s stopped" %(self.name)

	def pRestart(self):
		self.stop()
		#self.start()

	def pLoadconfig(self):
		self.conf['start'] = 1
		if 'debug' in self.app:
			self.conf['debug'] = self.app['debug']

	def pHelp(self, args = []):
		help = '* Available plugins :'
		for plug in self.app['plugins']:
			if self.app['plugins'][plug].running == True:
				help += '\n' + plug + ' help'
		return help + '\n\n' + plugin.PluginThread.pHelp(self, args)
