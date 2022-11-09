
# APMToBurp


## What is this?

This is a [Burp Suite](https://portswigger.net/burp/) extension that helps
security testers consult observability data while performing a security
assessment. 

This Burp Sutie extension was presented at BSides Lisbon 2022.

This project is licensed under the terms of the MIT license.

## Installing

Using it should be straightforward. In a running Burp Suite, go to:
  - Extender tab
  - then Extensions tab
  - click the Add button
  - in the new window, change Extension Type to Python
  - choose `APMToBurp.py` from this repository
  - click Next
  - click Close

## Using

When activated the extension injects APM headers in each proxied request. Pick
one, toggle _Original Request_ to _Edited Request_ and right click on the raw
request. 

The contextual menu will display:

  _Extensions_ -> _APMToBurp-> _Open in APM_

Click _Open in APM_ and the trace will show up in your default browser.

