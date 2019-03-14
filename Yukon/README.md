Script to obtain Yukon hansards.

Runs in the commandline, either hansard at a time or as a loop:

**
python3 get_yukon_hansards.py 1
**

**
for i in {1..100}; do python3 get_yukon_hansards.py $i; done
**

The number corresponds to the day of the legislature. For example, legislature 33 will run from day 1 to day 273, so the loop will iterate as such: {1..273}.

For each legislature, small edits needs to be made to the code. These are documented in the python script.


