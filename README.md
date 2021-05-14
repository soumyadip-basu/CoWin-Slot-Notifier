# CoWin-Slot-Notifier
Real time queries to the CoWIN public API  with cross state/district center selection to find available vaccine slots

ver 0.1
Utility to query the CoWIN database using the public API to find open vaccination slots in near real time (max 10 sec delay)

* Can select multiple vaccination centers, across states/districts, to monitor. 
  Select states, district and centres on the left panel. The selected centers will show up on the right panel.
* Pings the API every 10 secs. Logs shown in the bottom panel.
* If slot found, will sound an alarm, and show center, date and no.of slots in the bottom panel.
* Windows utility
