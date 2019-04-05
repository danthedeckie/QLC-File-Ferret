QLC+ File Ferret
================

**WARNING! VERY EARLY PROTOTYPE! NOT READY FOR PRODUCTION USE!!!**

We use QLC+ a lot.

We tend to have a single 'base' file, and then make specialised files per
event.

We have a few problems:

- Our 'base' file tends to get quite messy
- There's no easy way to move functions from a specialised file back into
  the base, or if one operator makes a cool sequence for a specific dance
  in one file, to move it to another.

This utility will try to help.

So far:
-------

Can move functions (scenes, chasers, collections, sequences, shows) from one
file to another.

**WARNING!**

It doesn't yet have any concept of moving fixtures around - so if you have
different fixtures in your different files, I have no clue what will happen.

Next:
-----

1) It has the capacity to see which functions are 'orphans' - not used by any
   other function, or attached to anything in the Virtual Console.  There should
   be a way to display that, and clean it up.

2) We need a TON of tests to confirm that it's not gonna screw up our files.
   This has only been made as a quick few-hours-between-shows hacky prototype.

3) Searching / Filtering / Sorting of functions by name,
   and by orphan-parent status.

4) Creating / Moving / Renaming Functions, with some semblance of automation,
   to allow (say) moving all functions used ONLY by a chaser into a folder of
   the same name, or renaming them all to helpful things...

5) Fixture aware!  So checking files are compatible (have compatible fixtures)
   or at least figuring out what to do when there are differences.

6) Make it prettier.  Icons, statusbar, etc.

To use:
-------

    python3 gui.py

And you can probably figure it out.
