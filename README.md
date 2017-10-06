# EOScmd

Python script to run on EOS.

Used for example with Telegraf and get the correct interface rate
./EOS_runcmd.py -H 10.10.10.10 -c "show interfaces Ethernet 1-24 counters rates" -p 80 -u None
