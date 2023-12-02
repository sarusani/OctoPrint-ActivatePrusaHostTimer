# Activate PrusaHost Timer

Plugin for OctoPrint to activate Prusa host features.

### Features
- Sends M79 S"OP" to the printer every x seconds
- Interval is configurable (5, 10, 15, 20 or 25 seconds)
- Interval can be paused

By installing this plugin, the following features (and more) will be available to you as soon as they are released with the newest Prusa firmware.

### Examples
#### Reprint
In the newest firmware (**not yet publicly available - planned for FW 3.14.0**), a Reprint menu item on the printer will be added.\
(Only shown when OctoPrint is sending the M79 command at least every 30 seconds)

This allows you to trigger a reprint of the last print job directly from the printer without going back to OctoPrint.
So you can remove a finished print, clean your print bed and then start a reprint directly from the printer without the need to open OctoPrint.

#### Set Ready
In the newest firmware (**not yet publicly available - planned for FW 3.14.0**), the Set Ready menu item on the printer will be added.\
(Only shown when OctoPrint is sending the M79 command at least every 30 seconds)

This will send the action "action:ready" to OctoPrint.
By using the [Action Commands](https://plugins.octoprint.org/plugins/actioncommands/) plugin you can setup OctoPrint to start the currently loaded print job.

This allows you to select a print job in OctoPrint, then setup you printer (load filament etc.) and then start the print job from the printer menu without the need to open OctoPrint again.

You can setup Action Commands to start the currently loaded print job by adding the following entry:
<img src="/extras/img/actionCommand-ready.png" width="700px" alt="Screenshot of Action Commands setting" />

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/sarusani/OctoPrint-ActivatePrusaHostTimer/archive/master.zip
