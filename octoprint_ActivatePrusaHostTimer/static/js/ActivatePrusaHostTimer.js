/*
 * View model for OctoPrint-ActivatePrusaHostTimer
 *
 * Author: sarusani
 * License: AGPLv3
 */
$(function() {
    function ActivatePrusaHostTimerViewModel(parameters) {
        var self = this;
        self.terminal = parameters[0];

        self.commandString = 'M79 S"OP"'

        self.terminal.command(self.commandString);        

        var intervalId = window.setInterval(function(){
            self.terminal.sendCommand();
        }, 10000);
    }

    // view model class, parameters for constructor, container to bind to
    OCTOPRINT_VIEWMODELS.push([
        ActivatePrusaHostTimerViewModel,
        ["terminalViewModel"],
    ]);
});
