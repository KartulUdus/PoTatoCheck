# PoTatoCheck

This is a tool designed to check if an account is able to sign in to PTC

⚠️ Potato doesnt check if banned, potato checks if valid and verified⚠️ 

# Install

To run you must have:

* python 2.7+
* installed requirements (`pip install -r requirements.txt --upgrade`)
* PhantomJs ([General instructions](PhantomJsInstructions.md))


# Password changer:


have your accounts ready in this format in the root of the project named
accounts.csv:
```
ptc,user,pass
ptc,user2,pass2
```
Run with:
`python password-changer.py -ac accounts.csv -pwd NewP4SSword! -of changed.csv`

Console logs will show unsuccessful changes and store new accounts file in 
changed.csv.

Should you wish to ignore accounts that could not sign in, run with `-ib` 
argument

Available arguments for password-changer can also be placed in 
`/config/config.ini`
examples available in `config/config.ini.example`

# Account login check:

have your accounts ready in this format in the root of the project named
accounts.csv:
```
ptc,user,pass
ptc,user2,pass2
```
Run with:
`python logincheck.py -ac accounts.csv`

If you want your output in a file, please run

`python logincheck.py -ac accounts.csv >verifeid.csv `

Default timeout to successfully log in is 5 seconds, but you happen to be doing
 this on a :potato: you can increase timeout with:
`python logincheck.py -ac accounts.csv -t 10`

Accounts that succesfully signed in will be printed in your console in the same
format as input file

Should you wish to ignore accounts that haven't verified the e-mail (yet) use:

`python logincheck.py -ac accounts.csv -t 10 -iu`


