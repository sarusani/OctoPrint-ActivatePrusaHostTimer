/*
 * Activate Prusa HostTimer
 *
 * Author: sarusani
 * License: AGPLv3
 */
$(function() {
    function id(name) {
        return `ActivatePrusaHostTimer_${name}`
    }

    function ActivatePrusaHostTimerViewModel(parameters) {
        var self = this;

        self.settingsViewModel = parameters[0];

        self.getSetting = function (path) {
            const setting_path = []
            if (typeof path === "string") {
                setting_path.push(path)
            } else {
                setting_path.push(...path)
            }

            let current = self.settingsViewModel.settings.plugins.ActivatePrusaHostTimer

            setting_path.forEach((setting) => {
                current = current[setting]
            })

            return current
        }

        self.sendCommand = function() {
            self.interval = self.getSetting("interval")();
            if(self.intervalId && self.oldInterval && self.oldInterval != self.interval) {
                clearInterval(self.intervalId);

                self.intervalId = window.setInterval(function(){
                    self.sendCommand();
                }, self.interval);
            }
            self.oldInterval = self.interval;

            if(!self.getSetting("paused")()) {
                OctoPrint.control.sendGcode('M79 S"OP"');
            }
        };

        self.onAfterBinding = function() {
            self.sendCommand();

            self.intervalId = window.setInterval(function(){
                self.sendCommand();
            }, self.interval);
        }
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: ActivatePrusaHostTimerViewModel,
        dependencies: ["settingsViewModel"],
        elements: ["#settings_plugin_ActivatePrusaHostTimer"]
    });
});
