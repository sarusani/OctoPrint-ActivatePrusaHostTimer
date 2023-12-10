# Activate Prusa HostTimer

OctoPrint plugin to activate Prusa host features.

## Features
- Sends M79 S"OP" to the printer in configurable intervals (5, 10, 15, 20 or 25 seconds)
- Interval ping can be paused
- Intercept action commands intended for PrusaLink and trigger corresponding OctoPrint features (if available)
- Printer notifications for "Set Ready" and "Reprint"

Supported printer models:<br />
[MK3S/+](https://github.com/prusa3d/Prusa-Firmware/releases) (Firmware 3.14.0 and newer)

### Examples
#### Reprint
Use the "Reprint" menu item on the printer to trigger a reprint of the last print job directly from the printer, without going back to OctoPrint.<br />
(The "Reprint" menu entry is only visible while the plugin is active.)

So you can remove a finished print, clean your print bed and then start a reprint directly from the printer.

#### Set Ready
Use the "Set Ready" menu item on the printer to tell OctoPrint to start a new print.<br />
(The "Set Ready" menu entry is only visible while the plugin is active.)

This will send the action "action:ready" to OctoPrint.<br />
Since this action is unknown to OctoPrint, the plugin will intercept it and start printing the currently selected file.<br />
(Can be deactivated in the plugin settings.)

It allows you to select a file in OctoPrint, setup you printer (load filament etc.) and then start the print job from the printer menu without the need to open OctoPrint again.

#### Notifications
Get printer notifications in OctoPrint whenever the printer triggers a print or toggles the status between "Ready" and "Not Ready".<br />
(Can be deactivated in the plugin settings.)
<br />
<br />
___
## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/sarusani/OctoPrint-ActivatePrusaHostTimer/archive/master.zip
