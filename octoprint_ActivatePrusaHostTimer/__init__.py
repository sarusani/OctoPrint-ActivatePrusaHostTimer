# coding=utf-8
import octoprint.plugin
import octoprint.util
import os
import sys

import flask
from flask_babel import gettext
from octoprint.access import USER_GROUP
from octoprint.access.permissions import Permissions
from octoprint.events import Events

class Prompt:
    def __init__(self, text):
        self.text = text
        self.choices = []

        self._active = False

    @property
    def active(self):
        return self._active

    def add_choice(self, text):
        self.choices.append(text)

    def activate(self):
        self._active = True

    def validate_choice(self, choice):
        return 0 <= choice < len(self.choices)

class ActivatePrusaHostTimerPlugin(
	octoprint.plugin.SettingsPlugin,
	octoprint.plugin.AssetPlugin,
	octoprint.plugin.TemplatePlugin,
	octoprint.plugin.StartupPlugin,
	octoprint.plugin.SimpleApiPlugin
	):

	def __init__(self):
		self._prompt = None
	
	def get_settings_defaults(self):
		return {
			"interval":20,
			"paused":0
		}
	
	def get_assets(self):
		return dict(
			js=["js/ActivatePrusaHostTimer.js"],
			clientjs=["clientjs/ActivatePrusaHostTimer.js"],
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

	def get_additional_permissions(self):
		return [
			{
				"key": "INTERACT",
				"name": "Interact with printer prompts",
				"description": gettext("Allows to see and interact with printer prompts"),
				"default_groups": [USER_GROUP],
				"roles": ["interact"]
			}
		]

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
			self._actionReady()

		if action == "not_ready":
			self._logAction(action)
			self._actionNotReady()
		
		return
	
	def _actionReady(self):
		self._printer.commands('M72 S1')
		self._printer.commands('M118 //action:notification Printer is ready.')
		#self._printer.start_print()

		if self._prompt is None:
			return		
		self._close_prompt()
		self._prompt = None

	def _actionNotReady(self):
		self._printer.commands('M72 S0')
		self._prompt = Prompt("Printer not ready to receive print jobs.")
		self._prompt.add_choice("Set printer state to ready")
		self._prompt.add_choice("Close")
		self._show_prompt()
	
	def _logAction(self, action):
		self._logger.info("Action intercepted: 'action:%s'" % (action))
	
	def on_event(self, event, payload):
		self._logger.info("on_event")
		if event == Events.DISCONNECTED:
			self._close_prompt()
	
	def get_api_commands(self):
		self._logger.info("get_api_commands")
		return {"select": ["choice"]}
	
	def on_api_command(self, command, data):
		self._logger.info("on_api_command")
		if command == "select":
			if not Permissions.PLUGIN_ACTIVATEPRUSAHOSTTIMER_INTERACT.can():
				return flask.abort(403)
			
			if self._prompt is None:
				return flask.abort(409, description="No active prompt")
			
			choice = data["choice"]
			if not isinstance(choice, int) or not self._prompt.validate_choice(choice):
				return flask.abort(400, f"{choice!r} is not a valid value for choice")
			
			self._answer_prompt(choice)
	
	def on_api_get(self, request):
		self._logger.info("on_api_get")
		if not Permissions.PLUGIN_ACTIVATEPRUSAHOSTTIMER_INTERACT.can():
			return flask.abort(403)
		if self._prompt is None:
			return flask.jsonify()
		else:
			return flask.jsonify(text=self._prompt.text, choices=self._prompt.choices)
	
	def _show_prompt(self):
		self._logger.info("_show_prompt")
		self._prompt.activate()
		self._plugin_manager.send_plugin_message(
			self._identifier,
			{
				"action": "show",
				"text": self._prompt.text,
				"choices": self._prompt.choices
			}
		)
		
	def _close_prompt(self):
		self._logger.info("_close_prompt")
		self._prompt = None
		self._plugin_manager.send_plugin_message(self._identifier, {"action": "close"})

	def _answer_prompt(self, choice):
		self._logger.info("_answer_prompt")
		self._logger.info(choice)
		if(choice == 0):
			self._actionReady()

		self._close_prompt()


__plugin_name__ = "Activate Prusa HostTimer"
__plugin_pythoncompat__ = ">=3.7,<4"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = ActivatePrusaHostTimerPlugin()
	
	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
		"octoprint.comm.protocol.action": __plugin_implementation__.action_handler,
		"octoprint.access.permissions": __plugin_implementation__.get_additional_permissions
	}
