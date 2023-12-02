# Activate PrusaHost Timer

Plugin for Octoprint to activate Prusa host features.

#### Features
- Sends M79 S"OP" to the printer every x seconds
- Interval is configurable (5, 10, 15, 20 or 25 seconds)
- Interval can be paused

#### Examples
In the newest firmware (**not yet publicly available**), a reprint menu item on the printer has been added.
(Only shown when OctoPrint is sending the M79 command at least every 30 seconds)

This allows you to trigger a reprint of the last print job directly from the printer without going back to OctoPrint.
So you can remove a finished print, clean your print bed and then start a reprint directly from the printer without the need to open OctoPrint.

By installing this plugin, this feature (and more) will be available to you as soon as the new firmware is released.

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/sarusani/OctoPrint-ActivatePrusaHostTimer/archive/master.zip
