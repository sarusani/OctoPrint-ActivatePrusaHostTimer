/*
 * View model for OctoPrint-ActivatePrusaHostTimer
 *
 * Author: sarusani
 * License: AGPLv3
 */
$(function() {
    function ActivatePrusaHostTimerViewModel() {
        var self = this;
        self.commandString = 'M79 S"OP"'

        var intervalId = window.setInterval(function(){
            OctoPrint.control.sendGcode(self.commandString);
        }, 10000);
    }

    ActivatePrusaHostTimerViewModel()
});
