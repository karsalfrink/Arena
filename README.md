ARENA - Java Package for Simulating Original D&D Combat
========================================================

This code package provides routines for simulating combat in
a tabletop Fantasy Role-Playing Game (FRPG) similar to Original D&D
or closely-related games. Combat is done as per "theater of the mind"
without tracking exact spatial locations; targets of attacks
are chosen by random method (as per 1E AD&D DMG). 
In most cases, the intent here is to output aggregate statistics based on 
many trials of the game between men and monsters. This package provides only 
command-line, text output; there are no graphics or visualizations, 
and generally few options for output regarding individual combats. 

For a precompiled JAR executable made from this package, and full 
JavaDoc pages, visit:

- http://www.oedgames.com/addons/houserules/software.html

The package currently includes five top-level main applications:

-----------------------------------------------------------------

ATHENA -- A master program that can initiate any of the applications below. 
Used as the main application in the combined JAR distribution.

ARENA -- Simulates a population of fighters, battling for
experience and treasure over some amount of time (broadly inspired by 
Roman arena-style events). Combat can be man vs. man or man vs.
monster, including simulated excursions against dungeon random 
encounters; individual combats can be one-on-one or in groups. Statistics
at the end show level-based demographics of the overall surviving population,
percent of experience from treasure, and number and ratio of deaths
caused by each type of monster in the database. 

MONSTER METRICS -- Performs a binary search at each fighter level 1-12
to determine how many fighters represent a matched challenge against
each monster in the database (i.e., closest to a 50/50 victory chance); 
then takes a harmonic mean across all levels to suggest an
Equivalent Hit Dice (EHD) value, to be used for balancing and
experience purposes. More detail available (per-level values and charts)
with command-line switches.

MARSHAL -- Creates random bands of men as encountered in the wilderness
(e.g., bandits, brigands, buccaneers, nomads, etc., in numbers 30-300),
with leaders of generally appropriate levels. The leaders are generated
by simulating their entire combat history in the Arena. 

NPC GENERATOR -- A minimalist command-line UI to generate characters
of any type as per OED rules. The characters, including thieves, wizards,
multiclass elves, etc., are generated by a simulated heuristic, not via
the Arena above (i.e., different from the Marshal process). Includes
simple magic items, spells for wizards, OED feats, and suggested
personalities keyed off alignment. (Depends on Apache PDF Box library, 
so make sure that's on your classpath; current version at 
https://pdfbox.apache.org/.)

-----------------------------------------------------------------

GPJ project files for use with jGRASP are included for each of the
applications above. It's easiest to simply use **Athena.gpj** to build the master 
program and all the child applications. 

While common monster special abilities are modeled, we have not implemented 
magic-user/wizard spells (so: no mixed PC parties with wizards, nor NPC wizard 
opponents). One round of special attacks is allowed for monster abilities
at the start of combat (e.g., dragon breath, giant boulders, medusa gaze, etc.). 

To the extent that the original rules are ambiguous or in need of DM
adjudication (as in many cases), the author has attempted to research 
and interpret the rules such as possible, and uses interpretations
as expressed in the Original Edition Delta (OED) House Rules set. In some
cases, software switches allow toggling between different modes. See
www.oedgames.com for more information. 

- Daniel R. Collins ("Delta")
www.oedgames.com
