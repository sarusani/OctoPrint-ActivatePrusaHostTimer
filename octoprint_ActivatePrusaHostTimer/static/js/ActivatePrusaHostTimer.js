/*
 * Activate Prusa HostTimer
 *
 * Author: sarusani
 * License: AGPLv3
 */
$(function() {
    function ActivatePrusaHostTimer() {
        var self = this;
        self.commandString = 'M79 S"OP"'
        
        OctoPrint.control.sendGcode(self.commandString);

        var intervalId = window.setInterval(function(){
            OctoPrint.control.sendGcode(self.commandString);
        }, 10000);
    }

    ActivatePrusaHostTimer()
});
