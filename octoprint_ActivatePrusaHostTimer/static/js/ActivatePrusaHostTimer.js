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
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: ActivatePrusaHostTimerViewModel,
        dependencies: ["settingsViewModel"],
        elements: ["#settings_plugin_ActivatePrusaHostTimer"]
    });
});
