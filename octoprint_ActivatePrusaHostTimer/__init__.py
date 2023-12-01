# coding=utf-8
import octoprint.plugin

class ActivatePrusaHostTimerPlugin(
	octoprint.plugin.SettingsPlugin,
	octoprint.plugin.AssetPlugin,
	octoprint.plugin.TemplatePlugin
	):

	def get_settings_defaults(self):
		return {
			"interval":10000,
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
				displayName="Activate Prusa HostTimer Plugin",
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


__plugin_name__ = "Activate Prusa HostTimer Plugin"
__plugin_pythoncompat__ = ">=3.7,<4"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = ActivatePrusaHostTimerPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
