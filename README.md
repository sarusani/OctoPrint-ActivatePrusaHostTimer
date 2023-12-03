# Activate Prusa HostTimer

OctoPrint plugin to activate Prusa host features.

### Features
- Sends M79 S"OP" to the printer every x seconds
- Interval is configurable (5, 10, 15, 20 or 25 seconds)
- Interval ping can be paused
- Intercept action commands intended for PrusaLink and trigger corresponding OctoPrint features (if available).

By installing this plugin, the following features (and more) will be available to you as soon as they are released with the newest Prusa firmware.

### Examples
#### Reprint
In the newest firmware (**not yet publicly available - planned for FW 3.14.0**), a Reprint menu item on the printer will be added.\
(Only shown when OctoPrint is sending the M79 command at least every 30 seconds)

This allows you to trigger a reprint of the last print job directly from the printer, without going back to OctoPrint.
So you can remove a finished print, clean your print bed and then start a reprint directly from the printer.

#### Set Ready
In the newest firmware (**not yet publicly available - planned for FW 3.14.0**), the Set Ready menu item on the printer will be added.\
(Only shown when OctoPrint is sending the M79 command at least every 30 seconds)

This will send the action "action:ready" to OctoPrint.
Since this action is unknown to OctoPrint, the plugin will intercept it and start the currently loaded print job.

This allows you to select a print job in OctoPrint, setup you printer (load filament etc.) and then start the print job from the printer menu without the need to open OctoPrint again.

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/sarusani/OctoPrint-ActivatePrusaHostTimer/archive/master.zip
