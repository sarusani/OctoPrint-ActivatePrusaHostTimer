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
			"detected_printer_model": "",
			"interval": 20,
			"paused": 0,
			"start_on_ready": 1,
			"show_notifications": 1
		}
	
	def get_assets(self):
		return {
			"js": ["js/ActivatePrusaHostTimer.js"],
			"css": ["css/ActivatePrusaHostTimer.css"]
		}
	
	def get_update_information(self):
		return {
			"ActivatePrusaHostTimer": {
				"displayName": "Activate Prusa HostTimer",
				"displayVersion": self._plugin_version,
				# version check: github repository
				"type": "github_release",
				"user": "sarusani",
				"repo": "OctoPrint-ActivatePrusaHostTimer",
				"current": self._plugin_version,
				"stable_branch": {
					"name": "Stable",
					"branch": "main",
					"comittish": ["main"]
				},
				"prerelease_branches": [
					{
						"name": "Release Candidate",
						"branch": "release-candidate",
						"comittish": ["release-candidate", "main"]
					}
				],
				#Update method: pip
				"pip": "https://github.com/sarusani/OctoPrint-ActivatePrusaHostTimer/archive/{target_version}.zip"
			}
		}

	def on_after_startup(self):
		#Try to detect printer model automatically if not alrady set
		self._detectPrinterModelName()

		#Start RepeatedTimer
		interval = self._settings.get_int(["interval"])	
		self._oldInterval = interval
		
		self._loop = octoprint.util.RepeatedTimer(interval, self._sendPing, run_first=True)
		self._loop.start()

	def action_handler(self, comm, line, action, *args, **kwargs):
		if ";" in action:
			action = action.split(";")[0]
			action = action.strip()
		
		if action == "ready" or action == "start":
			self._logAction(action)

			if self._settings.get_boolean(["start_on_ready"]) or action == "start":
				currentJob = self._printer.get_current_job().get("file").get("name")
				if currentJob is not None:
					self._showNotification("Printer is ready. Printing: %s" % (currentJob))
					self._startPrint(currentJob, action)
					return
				
				self._showNotification("Printer is ready, but there's no file selected.")
				return
			
			#Set printer state "ready"
			self._sendReadyState(1)
			self._showNotification("Printer is ready.")
			return

		if action == "not_ready":
			self._logAction(action)

			#Set printer state "not ready"
			self._sendReadyState(0)
			self._showNotification("Printer is not ready to receive print jobs.")
			return
		
		return
	
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
	
	def _detectPrinterModelName(self):
		profileModelName = "unknown"
		printerModel = "mk3s"
		printerProfile =  self._printer_profile_manager.get_current_or_default()
		
		if printerProfile is not None and printerProfile.get("model") != "":
			profileModelName = printerProfile.get("model")
		
		if not "mk3" in profileModelName.casefold():
			printerModel = profileModelName

		self._settings.set(["detected_printer_model"], printerModel)
		self._settings.save(trigger_event=True)

	def _sendReadyState(self,state):
		self._printer.commands("M72 S%s" % (state))

	def _showNotification(self, text):
		if self._settings.get_boolean(["show_notifications"]):
			self._printer.commands("M118 A1 action:notification %s" % (text))
	
	def _startPrint(self, currentJob, action=""):
		#Do not start a print if the printer is not OPERATIONAL or action:start was the source. (OctoPrint has native support for action:start)
		if self._printer.get_state_id() == "OPERATIONAL" and action != "start":
			self._logger.info("Starting print of %s" % (currentJob))
			self._printer.start_print()

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
