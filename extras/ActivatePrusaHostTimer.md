---
layout: plugin

id: ActivatePrusaHostTimer
title: OctoPrint-ActivatePrusaHostTimer
description: Plugin for Octoprint to activate Prusa host features
author: sarusani
license: AGPLv3

date: 2023-12-01

homepage: https://github.com/sarusani/OctoPrint-ActivatePrusaHostTimer
source: https://github.com/sarusani/OctoPrint-ActivatePrusaHostTimer
archive: https://github.com/sarusani/OctoPrint-ActivatePrusaHostTimer/archive/master.zip

follow_dependency_links: false

tags:
- prusa

compatibility:
  # list of compatible versions, for example 1.2.0. If left empty no specific version requirement will be assumed
  octoprint:
  - 1.2.0

  # list of compatible operating systems, valid values are linux, windows, macos, leaving empty defaults to all
  os:
  - linux
  - windows
  - macos
---

# OctoPrint-ActivatePrusaHostTimer

Plugin for Octoprint to activate Prusa host features.

Features:
- Sends M79 S"OP" to printer every 10 seconds

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/sarusani/OctoPrint-ActivatePrusaHostTimer/archive/master.zip
