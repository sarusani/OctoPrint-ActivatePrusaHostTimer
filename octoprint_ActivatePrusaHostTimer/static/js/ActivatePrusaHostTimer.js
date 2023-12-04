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

        self.settingsViewModel = parameters[2];

        self.loginState = parameters[0];
        self.access = parameters[1];

        self.modal = ko.observable(undefined);

        self.text = ko.observable();
        self.buttons = ko.observableArray([]);

        self.active = ko.pureComputed(function () {
            return self.text() !== undefined;
        });
        self.visible = ko.pureComputed(function () {
            return self.modal() !== undefined;
        });

        self.requestData = function () {
            if (
                !self.loginState.hasPermission(
                    self.access.permissions.PLUGIN_ACTIVATEPRUSAHOSTTIMER_INTERACT
                )
            )
                return;
            OctoPrint.plugins.ActivatePrusaHostTimer.get().done(self.fromResponse);
        };

        self.fromResponse = function (data) {
            if (data && data.hasOwnProperty("text") && data.hasOwnProperty("choices")) {
                self.text(data.text);
                self.buttons(data.choices);
                self.showPrompt();
            } else {
                self.text(undefined);
                self.buttons([]);
            }
        };

        self.showPrompt = function () {
            var text = self.text();
            var buttons = self.buttons();

            var opts = {
                title: gettext("Message from your printer"),
                message: text,
                selections: buttons,
                maycancel: true, // see #3171
                onselect: function (index) {
                    if (index > -1) {
                        self._select(index);
                    }
                },
                onclose: function () {
                    self.modal(undefined);
                }
            };

            self.modal(showSelectionDialog(opts));
        };

        self._select = function (index) {
            OctoPrint.plugins.ActivatePrusaHostTimer.select(index);
        };

        self._closePrompt = function () {
            var modal = self.modal();
            if (modal) {
                modal.modal("hide");
            }
        };

        self.onStartupComplete = function () {
            self.requestData();
        };
        
        self.onDataUpdaterPluginMessage = function (plugin, data) {
            if (
                !self.loginState.hasPermission(
                    self.access.permissions.PLUGIN_ACTIVATEPRUSAHOSTTIMER_INTERACT
                )
            )
                return;
            if (plugin !== "ActivatePrusaHostTimer") {
                return;
            }

            switch (data.action) {
                case "show": {
                    self.text(data.text);
                    self.buttons(data.choices);
                    self.showPrompt();
                    break;
                }
                case "close": {
                    self.text(undefined);
                    self.buttons([]);
                    self._closePrompt();
                    break;
                }
            }
        };
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: ActivatePrusaHostTimerViewModel,
        dependencies: ["loginStateViewModel", "accessViewModel","settingsViewModel"],
        elements: ["#settings_plugin_ActivatePrusaHostTimer", "#navbar_plugin_ActivatePrusaHostTimer"]
    });
});
