# PoTatoCheck

This is a tool designed to check if an account is able to sign in to PTC

# Install

To run you must have:

* python 2.7+
* configargparse (`pip install configargparse`)
* selenium (`pip install selenium`)
* PhantomJs (`npm install phantomjs`)
# Usage

have your accounts ready in this format in the root of the project named
accounts.csv:
```
ptc,user,pass
ptc,user2,pass2
```
Run with:
`python logincheck.py -ac accounts.csv`

Default timeout to successfully log in is 5 seconds, but you happen to be doing
 this on a :potato: you can increase timeout with:
`python logincheck.py -ac accounts.csv -t 10`

Accounts that succesfully signed in will be printed in your console in the same
format as input file

Should you wish to ignore accounts that haven't verified the e-mail (yet) use:
`python logincheck.py -ac accounts.csv -t 10 -iu`