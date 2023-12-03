# coding=utf-8
import octoprint.plugin
import octoprint.util
import os
import sys

class ActivatePrusaHostTimerPlugin(
	octoprint.plugin.SettingsPlugin,
	octoprint.plugin.AssetPlugin,
	octoprint.plugin.TemplatePlugin,
	octoprint.plugin.StartupPlugin
	):
	
	def get_settings_defaults(self):
		return {
			"interval":20,
			"paused":0
		}
	
	def get_assets(self):
		return dict(
			js=["js/ActivatePrusaHostTimer.js"],
			css=["css/ActivatePrusaHostTimer.css"]
		)
	
	def get_update_information(self):
		return dict(
			ActivatePrusaHostTimer=dict(
				displayName="Activate Prusa HostTimer",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="sarusani",
				repo="OctoPrint-ActivatePrusaHostTimer",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/sarusani/OctoPrint-ActivatePrusaHostTimer/archive/{target_version}.zip"
			)
		)
	
	def _sendPing(self):
		interval = self._settings.get_int(["interval"])	
		paused = self._settings.get_boolean(["paused"])
		
		if self._oldInterval != interval:
			self._loop.cancel()
			self._loop = octoprint.util.RepeatedTimer(interval, self._sendPing, run_first=False)
			self._loop.start()
			
			self._oldInterval = interval
		
		if not paused:
			self._printer.commands('M79 S"OP"')
	
	def on_after_startup(self):
		interval = self._settings.get_int(["interval"])
		self._oldInterval = interval
		
		self._loop = octoprint.util.RepeatedTimer(interval, self._sendPing, run_first=True)
		self._loop.start()

	def action_handler(self, comm, line, action, *args, **kwargs):
		if ";" in action:
			action = action.split(';')[0]
			action = action.strip()

		if action == "ready":
			self._logAction(action)
			self._printer.start_print()
		
		return
	
	def _logAction(self, action):
		self._logger.info("Action intercepted: 'action:%s'" % (action))


__plugin_name__ = "Activate Prusa HostTimer"
__plugin_pythoncompat__ = ">=3.7,<4"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = ActivatePrusaHostTimerPlugin()
	
	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
		"octoprint.comm.protocol.action": __plugin_implementation__.action_handler
	}
