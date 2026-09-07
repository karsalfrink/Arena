# EHD comparison: Delving Deeper rows vs the master (OD&D/OED) database

Both columns are computed with the same Arena build (MonsterMetrics
spotlight mode, 1000 fights per point). 'Master stored' is the EHD in
MonsterDatabase.csv; 'master new' is the same row recomputed today, so
the DD value should be read against 'master new'. Stat differences
explain most gaps: DD monsters usually get one attack roll where OED
gives several, and DD's crit-damage pattern is not modelled.

| DD row | DD EHD | Master row | Master new | Master stored | DD stats | Master stats |
|---|---|---|---|---|---|---|
| Orc | 1 | Orc | 1 | 1 | AC 7 HD 1 Atk 1 Dam 1d6; - | AC 6 HD 1 Atk 1 Dam 1d6; LightSensitivity |
| Goblin | 1 | Goblin | 1 | 1 | AC 7 HD 1-1 Atk 1 Dam 1d6; - | AC 6 HD 1-1 Atk 1 Dam 1d3; LightSensitivity |
| Kobold | 1 | Kobold | 1 | 1 | AC 7 HD 1/2 Atk 1 Dam 1d6; Swimming (9) | AC 7 HD 1/2 Atk 1 Dam 1d3; LightSensitivity |
| Hobgoblin | 1 | Hobgoblin | 1 | 1 | AC 5 HD 1+1 Atk 1 Dam 1d6; - | AC 5 HD 1+1 Atk 1 Dam 1d6; Bravery (1) |
| Gnoll | 1 | Gnoll | 1 | 2 | AC 6 HD 2 Atk 1 Dam 1d6; - | AC 5 HD 2 Atk 1 Dam 1d6; Bravery (2) |
| Ogre | 3 | Ogre | 3 | 4 | AC 6 HD 4+1 Atk 1 Dam 1d6+2; - | AC 5 HD 4+1 Atk 1 Dam 1d6+2; - |
| Troll | 5 | Troll | 7 | 8 | AC 5 HD 6+3 Atk 1 Dam 1d6; Regeneration (3) | AC 4 HD 6+3 Atk 2 Dam 1d6; Regeneration (3) |
| Hill Giant | 8 | Hill Giant | 8 | 8 | AC 4 HD 8 Atk 1 Dam 2d6; RockHurling, Fearlessness | AC 4 HD 8 Atk 1 Dam 2d6; RockHurling |
| Stone Giant | 9 | Stone Giant | 8 | 9 | AC 2 HD 9 Atk 1 Dam 2d6; RockHurling, Fearlessness | AC 4 HD 9 Atk 1 Dam 2d6; RockHurling |
| Frost Giant | 10 | Frost Giant | 10 | 10 | AC 4 HD 10+1 Atk 1 Dam 2d6+1; RockHurling, Fearlessness, ColdImmunity | AC 4 HD 10+1 Atk 1 Dam 2d6+1; RockHurling, ColdImmunity |
| Fire Giant | 11 | Fire Giant | 11 | 11 | AC 3 HD 11+3 Atk 1 Dam 2d6+2; RockHurling, Fearlessness, FireImmunity | AC 4 HD 11+3 Atk 1 Dam 2d6+2; RockHurling, FireImmunity |
| Cloud Giant | 14 | Cloud Giant | 12 | 12 | AC 3 HD 12+2 Atk 1 Dam 3d6; RockHurling, Fearlessness, Detection | AC 4 HD 12+2 Atk 1 Dam 3d6; RockHurling, Detection |
| Storm Giant | 19 | Storm Giant | 18 | 17 | AC 2 HD 15 Atk 1 Dam 3d6+3; RockHurling, Fearlessness, VoltImmunity | AC 4 HD 15 Atk 1 Dam 3d6+3; RockHurling, WeatherControl |
| Titan | 38 | Titan | 40 | 40 | AC 2 HD 21 Atk 1 Dam 3d6+3; Spells | AC 2 HD 20 Atk 1 Dam 3d6+3; MagicResistance (60), Spells |
| Skeleton | 1 | Skeleton | 1 | 1 | AC 8 HD 1/2 Atk 1 Dam 1d6; Fearlessness | AC 7 HD 1 Atk 1 Dam 1d6; Fearlessness |
| Zombie | 1 | Zombie | 1 | 2 | AC 9 HD 1 Atk 1 Dam 1d6; Fearlessness | AC 8 HD 2 Atk 1 Dam 1d6; Fearlessness |
| Ghoul | 3 | Ghoul | 3 | 3 | AC 7 HD 2 Atk 1 Dam 1d6; Paralysis | AC 6 HD 2 Atk 1 Dam 1d6; Paralysis, Spawn |
| Wight | 3 | Wight | 3 | 3 | AC 6 HD 3 Atk 1 Dam 1d6; SilverToHit, EnergyDrain (1) | AC 5 HD 3 Atk 1 Dam 1d6; SilverToHit, EnergyDrain (1), Spawn |
| Wraith | 4 | Wraith | 4 | 4 | AC 4 HD 4 Atk 1 Dam 1d6; Flight (12), SilverToHit, ChopResistance (1), EnergyDrain (1), Fear (2) | AC 3 HD 4 Atk 1 Dam 1d6; Flight (24), SilverToHit, EnergyDrain (1), Spawn |
| Mummy | 6 | Mummy | 7 | 6 | AC 4 HD 5+1 Atk 1 Dam 1d6; MagicToHit (1), ChopResistance, FireVulnerability, Rotting | AC 3 HD 5+1 Atk 1 Dam 1d6; MagicToHit (1), ChopResistance, FireVulnerability, Rotting |
| Spectre | 7 | Spectre | 8 | 8 | AC 3 HD 6 Atk 1 Dam 1d6; Flight (15), MagicToHit (1), EnergyDrain (2) | AC 2 HD 6 Atk 1 Dam 1d6; Flight (30), MagicToHit (1), EnergyDrain (2), Spawn |
| Vampire | 24 | Vampire | 26 | 25 | AC 2 HD 8 Atk 1 Dam 1d6; Flight (18), MagicToHit (1), Regeneration (3), EnergyDrain (2), Charm (-2), SummonVermin, Polymorphism | AC 2 HD 8 Atk 1 Dam 1d6; Flight (12), MagicToHit (1), Regeneration (3), EnergyDrain (2), Charm (-2), Spawn, SummonVermin, GasForm, Polymorphism, Undying |
| Yellow Mold | 5 | Yellow Mold | 2 | 2 | AC 9 HD 3 Atk 1 Dam 1d6; SporeCloud, WoodEating, VoltImmunity, ColdImmunity, ChopImmunity | AC 9 HD 1 Atk 1 Dam 1d6; SporeCloud, WoodEating, VoltImmunity, ColdImmunity, ChopImmunity |
| Green Slime | 5 | Green Slime | 4 | 3 | AC 9 HD 3 Atk 1 Dam 0; FleshEating, WoodEating, MetalEating, VoltImmunity, ChopImmunity | AC 9 HD 2 Atk 1 Dam 0; FleshEating, WoodEating, MetalEating, VoltImmunity, ChopImmunity |
| Gray Ooze | 4 | Gray Ooze | 4 | 4 | AC 9 HD 3 Atk 1 Dam 2d6; MetalEating, FireImmunity, ColdImmunity | AC 8 HD 3 Atk 1 Dam 2d6; MetalEating, FireImmunity, ColdImmunity |
| Gelatinous Cube | 5 | Gelatinous Cube | 5 | 4 | AC 8 HD 4 Atk 1 Dam 1d6; Paralysis, VoltImmunity, ColdImmunity | AC 8 HD 4 Atk 1 Dam 1d6; Paralysis, VoltImmunity, ColdImmunity |
| Ochre Jelly | 4 | Ochre Jelly | 4 | 4 | AC 9 HD 5 Atk 1 Dam 1d6; WoodEating, VoltImmunity, ChopImmunity | AC 8 HD 5 Atk 1 Dam 1d6; WoodEating, VoltImmunity, ChopImmunity, Splitting |
| Black Pudding | 12 | Black Pudding | 13 | 13 | AC 7 HD 10 Atk 1 Dam 3d6; WoodEating, MetalEating, VoltImmunity, ColdImmunity, ChopImmunity | AC 6 HD 10 Atk 1 Dam 3d6; WoodEating, MetalEating, VoltImmunity, ColdImmunity, ChopImmunity, Splitting |
| Bear | 4 | Bear | 6 | 6 | AC 6 HD 5+5 Atk 1 Dam 1d6+2; - | AC 5 HD 6 Atk 2 Dam 1d6; Rending |
| Lion | 3 | Lion | 5 | 5 | AC 6 HD 5+2 Atk 1 Dam 1d6+1; - | AC 6 HD 5 Atk 2 Dam 1d6; Stealth (2), Rending |
| Sabre-Toothed Tiger | 5 | Sabre-Tooth Tiger | 7 | 7 | AC 6 HD 7+2 Atk 1 Dam 1d8+1; - | AC 6 HD 7+2 Atk 2 Dam 1d6+1; Stealth (2), Rending |
| Boar | 1 | Boar | 2 | 3 | AC 7 HD 1+2 Atk 1 Dam 1d6; - | AC 7 HD 3+3 Atk 1 Dam 1d6+1; - |
| Wolf | 1 | Wolf | 1 | 1 | AC 7 HD 1 Atk 1 Dam 1d6; - | AC 7 HD 2 Atk 1 Dam 1d6; - |
| Giant Wolf | 2 | Dire Wolf | 2 | 2 | AC 6 HD 2+2 Atk 1 Dam 1d6; - | AC 6 HD 3+3 Atk 1 Dam 1d6; - |
| Giant Rat | 1 | Giant Rat | 1 | 1 | AC 7 HD 1/2 Atk 1 Dam 1d3; Swimming (6) | AC 7 HD 1/2 Atk 1 Dam 1d3; Disease |
| Giant Centipede | 5 | Giant Centipede | 1 | 1 | AC 3 HD 3+1 Atk 1 Dam 1d6; Paralysis | AC 9 HD 1/3 Atk 1 Dam 0; Poison (4) |
| Giant Spider | 6 | Giant Spider | 6 | 6 | AC 5 HD 4+4 Atk 1 Dam 1d6; WebMove (12), Poison, Webs | AC 4 HD 4+4 Atk 1 Dam 1d6+2; Poison, WebMove (12) |
| Large Spider | 1 | Large Spider | 1 | 2 | AC 8 HD 1/2 Atk 1 Dam 1d6; Poison (2) | AC 8 HD 1+1 Atk 1 Dam 1d3; Poison (2) |
| Giant Scorpion | 6 | Giant Scorpion | 9 | 9 | AC 3 HD 5+4 Atk 1 Dam 1d6+2; Poison | AC 3 HD 5+5 Atk 3 Dam 1d6; Poison |
| Giant Toad | 3 | Giant Toad | 2 | 3 | AC 6 HD 2+4 Atk 1 Dam 1d6; Swimming (6), Poison | AC 6 HD 2 Atk 1 Dam 1d6; Leaping, Constriction, Poison |
| Giant Leech | 1 | Giant Leech | 1 | 2 | AC 8 HD 2 Atk 1 Dam 1d6; Swimming (6), EnergyDrain (1) | AC 8 HD 2 Atk 1 Dam 1d6+1; BloodDrain (2), Disease |
| Giant Weasel | 2 | Giant Weasel | 3 | 3 | AC 6 HD 2 Atk 1 Dam 1d6; BloodDrain (4) | AC 6 HD 3+3 Atk 1 Dam 1d6; BloodDrain (6) |
| Giant Lizard | 2 | Giant Lizard | 2 | 2 | AC 5 HD 3+1 Atk 1 Dam 1d6; - | AC 5 HD 3+1 Atk 1 Dam 1d6; - |
| Giant Crab | 2 | Giant Crab | 3 | 4 | AC 3 HD 3 Atk 1 Dam 1d6; - | AC 2 HD 3 Atk 2 Dam 1d6+1; - |
| Crocodile | 2 | Crocodile | 2 | 2 | AC 6 HD 3 Atk 1 Dam 1d6; Swimming (15) | AC 5 HD 3 Atk 1 Dam 1d6; Swimming (15) |
| Giant Crocodile | 7 | Giant Crocodile | 6 | 5 | AC 5 HD 7 Atk 1 Dam 2d6; Swimming (15), Swallowing | AC 5 HD 6 Atk 1 Dam 2d6; Swimming (15), Rending, Capsizing |
| Giant Viper | 7 | Giant Poisonous Snake | 5 | 5 | AC 6 HD 7 Atk 1 Dam 1d6; Swimming (9), Poison | AC 5 HD 4+2 Atk 1 Dam 1d6; Poison |
| Giant Constrictor Snake | 6 | Giant Constrictor Snake | 6 | 6 | AC 6 HD 7 Atk 1 Dam 2d6; Swimming (9), Constriction | AC 5 HD 6+1 Atk 1 Dam 1d6+2; Constriction |
| Giant Octopus | 4 | Giant Octopus | 4 | 5 | AC 7 HD 4 Atk 4 Dam 1d6; Swimming (9) | AC 7 HD 4 Atk 8 Dam 1d3; Swimming (9), Constriction, Jet, InkCloud |
| Giant Squid | 6 | Giant Squid | 9 | 11 | AC 7 HD 6 Atk 4 Dam 1d6; Swimming (12) | AC 7 HD 6 Atk 10 Dam 1d6; Swimming (12), Constriction, Jet, InkCloud |
| Mastodon | 10 | Mastodon | 16 | 16 | AC 6 HD 12 Atk 1 Dam 2d6+2; - | AC 6 HD 12 Atk 3 Dam 2d6; - |
| Tyrannosaurus Rex | 23 | Tyranosaurus Rex | 20 | 18 | AC 5 HD 20 Atk 1 Dam 4d6; Swallowing | AC 5 HD 20 Atk 1 Dam 4d6; - |
| Wight Ape | 4 | White Ape | 5 | 5 | AC 6 HD 5+2 Atk 1 Dam 2d6-1; - | AC 6 HD 6 Atk 2 Dam 1d6; - |
| Basilisk | 18 | Basilisk | 19 | 20 | AC 4 HD 6+1 Atk 1 Dam 1d6; PetrifyingGaze, Petrification | AC 4 HD 6+1 Atk 1 Dam 1d6; PetrifyingGaze, Petrification |
| Cockatrice | 6 | Cockatrice | 6 | 6 | AC 6 HD 5 Atk 1 Dam 1d6; Flight (18), Petrification | AC 6 HD 5 Atk 1 Dam 1d6; Flight (9), Petrification |
| Medusa | 11 | Medusa | 12 | 11 | AC 7 HD 4 Atk 1 Dam 1d6; PetrifyingGaze, Poison | AC 8 HD 4 Atk 2 Dam 1d6; PetrifyingGaze, Poison |
| Gorgon | 11 | Gorgon | 13 | 11 | AC 3 HD 8 Atk 1 Dam 1d6; PetrifyingBreath | AC 2 HD 8 Atk 1 Dam 2d6; PetrifyingBreath |
| Chimera | 11 | Chimera | 11 | 10 | AC 4 HD 9 Atk 3 Dam 1d6; Flight (18), FireBreath (3) | AC 4 HD 9 Atk 3 Dam 1d6; Flight (18), FireBreath (3) |
| Manticora | 5 | Manticore | 8 | 9 | AC 5 HD 6+1 Atk 1 Dam 1d6; Flight (18), TailSpikes | AC 4 HD 6+1 Atk 3 Dam 1d6; Flight (18), TailSpikes |
| Wyvern | 8 | Wyvern | 8 | 9 | AC 4 HD 7 Atk 1 Dam 1d6+2; Flight (24), Poison | AC 3 HD 7 Atk 1 Dam 1d6+2; Flight (24), Poison |
| Salamander | 10 | Salamander | 9 | 9 | AC 5 HD 7+3 Atk 1 Dam 2d6; Constriction, FireImmunity, MagicToHit (1) | AC 5 HD 7+3 Atk 2 Dam 2d6; Heat, Constriction, FireImmunity |
| Minotaur | 4 | Minotaur | 6 | 6 | AC 6 HD 6 Atk 1 Dam 1d6; Fearlessness | AC 6 HD 6 Atk 2 Dam 1d6+2; Fearlessness |
| Gargoyle | 3 | Gargoyle | 4 | 5 | AC 6 HD 4 Atk 1 Dam 1d6; Flight (15), MagicToHit (1) | AC 5 HD 4 Atk 2 Dam 1d6; Flight (15), MagicToHit (1) |
| Doppelganger | 3 | Doppleganger | 3 | 3 | AC 5 HD 4 Atk 1 Dam 1d6; Polymorphism, SaveBonus (6) | AC 5 HD 4 Atk 1 Dam 1d6+1; Polymorphism, SaveBonus (6) |
| Shadow | 2 | Shadow | 3 | 3 | AC 7 HD 2+2 Atk 1 Dam 1d6; Flight (9), SilverToHit, StrengthDrain | AC 7 HD 2+2 Atk 1 Dam 1d3; MagicToHit (1), StrengthDrain, Spawn, BlankMind |
| Purple Worm | 18 | Purple Worm | 22 | 22 | AC 6 HD 15 Atk 1 Dam 2d6; Swallowing, Poison, Fearlessness | AC 6 HD 15 Atk 2 Dam 2d6; Swallowing, Poison, Fearlessness |
| Dragon Turtle | 19 | Dragon Turtle | 25 | 25 | AC 2 HD 12 Atk 1 Dam 1d6; Swimming (9), SteamBreath | AC 2 HD 12 Atk 2 Dam 2d6; Swimming (9), Detection (15), Fear (2), SteamBreath |
| Gothrog | 25 | Balrog | 27 | 26 | AC 3 HD 10 Atk 2 Dam 2d6; Flight (15), MagicToHit (1), MagicResistance (75), FireImmunity, Immolation, Fearlessness | AC 2 HD 10 Atk 2 Dam 2d6; Flight (15), MagicToHit (1), MagicResistance (75), Immolation |
| Werewolf | 2 | Werewolf | 3 | 3 | AC 6 HD 4 Atk 1 Dam 1d6; SilverToHit | AC 5 HD 4 Atk 1 Dam 1d6; Lycanthropy, SilverToHit |
| Wereboar | 3 | Wereboar | 3 | 3 | AC 5 HD 4+1 Atk 1 Dam 1d6; SilverToHit | AC 4 HD 4+1 Atk 1 Dam 1d6; Lycanthropy, SilverToHit |
| Weretiger | 3 | Weretiger | 5 | 5 | AC 4 HD 5 Atk 1 Dam 1d6; SilverToHit | AC 3 HD 5 Atk 2 Dam 1d6; Lycanthropy, SilverToHit |
| Werebear | 4 | Werebear | 7 | 7 | AC 3 HD 6 Atk 1 Dam 1d6; SilverToHit | AC 2 HD 6 Atk 2 Dam 1d6; Lycanthropy, SilverToHit, Rending |
| Flesh Golem | 12 | Flesh Golem | 14 | 15 | AC 9 HD 9 Atk 1 Dam 2d6; MagicToHit (1), MagicImmunity | AC 9 HD 12 Atk 1 Dam 2d6; MagicToHit (1), MagicImmunity |
| Stone Living Statue | 42 | Stone Golem | 47 | 48 | AC 5 HD 14 Atk 1 Dam 3d6; Golem, MagicToHit (2), MagicImmunity, Slowing | AC 5 HD 18 Atk 1 Dam 3d6; MagicToHit (2), MagicImmunity, Slowing |
| Iron Living Statue | 120 | Iron Golem | 139 | 150 | AC 2 HD 18 Atk 1 Dam 4d6; Golem, MagicToHit (3), MagicImmunity, PoisonBreath (1) | AC 2 HD 25 Atk 1 Dam 4d6; MagicToHit (3), MagicImmunity, PoisonBreath (1) |
| Dwarf | 1 | Dwarf | 1 | 1 | AC 4 HD 1 Atk 1 Dam 1d6; DodgeGiants | AC 4 HD 1 Atk 1 Dam 1d6; SaveBonus (4), DodgeGiants |
| Elf | 1 | Elf | 1 | 1 | AC 7 HD 1 Atk 1 Dam 1d6; - | AC 5 HD 1+1 Atk 1 Dam 1d6; Camouflage, HitBonus (1) |
| Gnome | 1 | Gnome | 1 | 1 | AC 6 HD 1 Atk 1 Dam 1d6; - | AC 5 HD 1 Atk 1 Dam 1d6; SaveBonus (4), DodgeGiants |
| Pixie | 1 | Pixie | 1 | 1 | AC 6 HD 1-1 Atk 1 Dam 1d6; Flight (18), Invisibility, Sleep | AC 6 HD 1 Atk 1 Dam 1d3; Flight (18), Invisibility |
| Nixie | 1 | Nixie | 1 | 1 | AC 7 HD 1-1 Atk 1 Dam 1d6; Swimming (12), CharmPerTen | AC 7 HD 1 Atk 1 Dam 1d3; Swimming (9), CharmPerTen, Grappling |
| Dryad | 5 | Dryad | 5 | 5 | AC 5 HD 2 Atk 1 Dam 1d6; Charm (-2) | AC 5 HD 2 Atk 1 Dam 1d3; Charm (-2) |
| Centaur | 3 | Centaur | 3 | 4 | AC 6 HD 4 Atk 2 Dam 1d6; - | AC 5 HD 4 Atk 2 Dam 1d6; - |
| Unicorn | 3 | Unicorn | 5 | 6 | AC 3 HD 4 Atk 1 Dam 1d6; SaveBonus (6), Detection (24) | AC 2 HD 4 Atk 2 Dam 1d6+2; SaveBonus (6), Detection (24), DimensionDoor (36) |
| Pegasus | 2 | Pegasus | 2 | 2 | AC 6 HD 2+2 Atk 1 Dam 1d6; Flight (48) | AC 6 HD 2+2 Atk 2 Dam 1d6; Flight (48) |
| Hippogriff | 2 | Hippogriff | 3 | 3 | AC 6 HD 3+1 Atk 1 Dam 1d6; Flight (36) | AC 5 HD 3+1 Atk 2 Dam 1d6; Flight (36) |
| Griffon | 4 | Griffon | 8 | 8 | AC 4 HD 7 Atk 1 Dam 1d6; Flight (30) | AC 3 HD 7 Atk 2 Dam 1d6+2; Flight (30) |
| Treant | 33 | Treant | 26 | 25 | AC 2 HD 8 Atk 1 Dam 2d6; MagicToHit (1), ChopResistance, FireVulnerability, SummonTrees | AC 2 HD 8 Atk 2 Dam 2d6; SummonTrees |
| Animated Tree | 14 | Animated Tree | 10 | 10 | AC 2 HD 8 Atk 1 Dam 2d6; MagicToHit (1), ChopResistance, FireVulnerability | AC 2 HD 8 Atk 2 Dam 2d6; - |
| Young Roc | 4 | Small Roc | 5 | 5 | AC 6 HD 6 Atk 1 Dam 1d6; Flight (48) | AC 4 HD 6 Atk 2 Dam 1d6; Flight (48), Detection |
| Adult Roc | 9 | Medium Roc | 15 | 14 | AC 5 HD 12 Atk 1 Dam 2d6; Flight (42) | AC 4 HD 12 Atk 2 Dam 2d6; Flight (48), Detection |
| Ancient Roc | 22 | Large Roc | 25 | 24 | AC 4 HD 18 Atk 1 Dam 3d6; Flight (36), Fear (2) | AC 4 HD 18 Atk 2 Dam 3d6; Flight (48), Detection |
| Bandit | 1 | Bandit | 1 | 1 | AC 8 HD 1 Atk 1 Dam 1d6; - | AC 6 HD 1 Atk 1 Dam 1d6; - |
| Brigand | 1 | Brigand | 1 | 1 | AC 6 HD 1 Atk 1 Dam 1d6; - | AC 6 HD 1 Atk 1 Dam 1d6; Bravery (1) |
| Berserker | 1 | Berserker | 1 | 1 | AC 9 HD 1+1 Atk 1 Dam 1d6; HitBonus (2), Fearlessness | AC 7 HD 1+1 Atk 1 Dam 1d6; Fearlessness, HitBonus (2) |
| Dervish | 1 | Dervish | 1 | 1 | AC 8 HD 1+1 Atk 1 Dam 1d6; HitBonus (2), Fearlessness | AC 6 HD 1+1 Atk 1 Dam 1d6; Fearlessness, HitBonus (1) |
| Nomad | 1 | Nomad | 1 | 1 | AC 8 HD 1 Atk 1 Dam 1d6; - | AC 6 HD 1 Atk 1 Dam 1d6; - |
| Buccaneer | 1 | Buccaneer | 1 | 1 | AC 8 HD 1 Atk 1 Dam 1d6; - | AC 6 HD 1 Atk 1 Dam 1d6; - |
| Pirate | 1 | Pirate | 1 | 1 | AC 8 HD 1 Atk 1 Dam 1d6; - | AC 6 HD 1 Atk 1 Dam 1d6; - |
| Merman | 1 | Merman | 1 | 1 | AC 7 HD 1+1 Atk 1 Dam 1d6; Swimming (15) | AC 7 HD 1+1 Atk 1 Dam 1d6; Swimming (15), Grappling, LandWeakness |
| Caveman | 1 | Caveman | 1 | 2 | AC 9 HD 2 Atk 1 Dam 1d6; - | AC 9 HD 2 Atk 1 Dam 1d6+1; Cowardice |
| Djinni | 6 | Djinni | 6 | 7 | AC 6 HD 7+1 Atk 1 Dam 2d6-1; Flight (24), Invisibility, Illusion, Whirlwind (2) | AC 5 HD 7+1 Atk 1 Dam 2d6-1; Flight (24), Creation, Illusion, Invisibility, GasForm, Whirlwind (1) |
| Efreeti | 11 | Efreeti | 13 | 14 | AC 4 HD 10 Atk 1 Dam 2d6; Flight (24), Invisibility, Illusion, WallOfFire | AC 3 HD 10 Atk 1 Dam 2d6; Flight (24), Creation, Illusion, Invisibility, GasForm, WallOfFire |
| Invisible Stalker | 7 | Invisible Stalker | 8 | 8 | AC 2 HD 8 Atk 1 Dam 1d6; Flight (12), Invisibility | AC 3 HD 8 Atk 1 Dam 1d6+2; Invisibility, Tracking |
| Eight Hit Dice Air Elemental | 7 | Small Air Elemental | 10 | 10 | AC 3 HD 8 Atk 1 Dam 1d6+1; Flight (36), Whirlwind (3), MagicToHit (1) | AC 2 HD 8 Atk 1 Dam 1d6; Flight (36), Whirlwind (3), MagicToHit (2) |
| Twelve Hit Dice Air Elemental | 11 | Medium Air Elemental | 18 | 18 | AC 3 HD 12 Atk 1 Dam 1d6+1; Flight (36), Whirlwind (3), MagicToHit (1) | AC 2 HD 12 Atk 1 Dam 1d6; Flight (36), Whirlwind (3), MagicToHit (2) |
| Sixteen Hit Dice Air Elemental | 15 | Large Air Elemental | 21 | 22 | AC 3 HD 16 Atk 1 Dam 1d6+1; Flight (36), Whirlwind (3), MagicToHit (1) | AC 2 HD 16 Atk 1 Dam 1d6; Flight (36), Whirlwind (3), MagicToHit (2) |
| Eight Hit Dice Earth Elemental | 11 | Small Earth Elemental | 17 | 18 | AC 3 HD 8 Atk 1 Dam 3d6; MagicToHit (1) | AC 2 HD 8 Atk 1 Dam 3d6; MagicToHit (2) |
| Twelve Hit Dice Earth Elemental | 18 | Medium Earth Elemental | 24 | 26 | AC 3 HD 12 Atk 1 Dam 3d6; MagicToHit (1) | AC 2 HD 12 Atk 1 Dam 3d6; MagicToHit (2) |
| Sixteen Hit Dice Earth Elemental | 26 | Large Earth Elemental | 36 | 36 | AC 3 HD 16 Atk 1 Dam 3d6; MagicToHit (1) | AC 2 HD 16 Atk 1 Dam 3d6; MagicToHit (2) |
| Eight Hit Dice Fire Elemental | 9 | Small Fire Elemental | 15 | 15 | AC 3 HD 8 Atk 1 Dam 2d6; MagicToHit (1) | AC 2 HD 8 Atk 1 Dam 2d6; MagicToHit (2) |
| Twelve Hit Dice Fire Elemental | 14 | Medium Fire Elemental | 21 | 20 | AC 3 HD 12 Atk 1 Dam 2d6; MagicToHit (1) | AC 2 HD 12 Atk 1 Dam 2d6; MagicToHit (2) |
| Sixteen Hit Dice Fire Elemental | 19 | Large Fire Elemental | 29 | 33 | AC 3 HD 16 Atk 1 Dam 2d6; MagicToHit (1) | AC 2 HD 16 Atk 1 Dam 2d6; MagicToHit (2) |
| Eight Hit Dice Water Elemental | 10 | Small Water Elemental | 13 | 15 | AC 3 HD 8 Atk 1 Dam 2d6; Swimming (18), MagicToHit (1) | AC 2 HD 8 Atk 1 Dam 2d6; Swimming (18), MagicToHit (2) |
| Twelve Hit Dice Water Elemental | 13 | Medium Water Elemental | 20 | 20 | AC 3 HD 12 Atk 1 Dam 2d6; Swimming (18), MagicToHit (1) | AC 2 HD 12 Atk 1 Dam 2d6; Swimming (18), MagicToHit (2) |
| Sixteen Hit Dice Water Elemental | 19 | Large Water Elemental | 32 | 33 | AC 3 HD 16 Atk 1 Dam 2d6; Swimming (18), MagicToHit (1) | AC 2 HD 16 Atk 1 Dam 2d6; Swimming (18), MagicToHit (2) |
| Draft Horse | 0 | Draft Horse | 1 | 2 | AC 7 HD 2+1 Atk 0 Dam 0; - | AC 7 HD 2+1 Atk 1 Dam 1d6; - |
| Mule | 0 | Mule | 1 | 2 | AC 7 HD 2 Atk 0 Dam 0; - | AC 7 HD 2+1 Atk 1 Dam 1d6; - |
| Riding Horse | 0 | Light Horse | 1 | 1 | AC 7 HD 2 Atk 0 Dam 0; - | AC 7 HD 2 Atk 1 Dam 1d6; - |
| War Horse | 1 | Medium Horse | 2 | 2 | AC 7 HD 2+2 Atk 1 Dam 1d6; - | AC 7 HD 2+1 Atk 2 Dam 1d6; - |
| Destrier | 2 | Heavy Horse | 3 | 3 | AC 7 HD 2+4 Atk 1 Dam 1d6; - | AC 7 HD 3 Atk 2 Dam 1d6; - |
| Five-Headed Hydra | 6 | Five-Headed Hydra | 7 | 6 | AC 5 HD 5 Atk 5 Dam 1d6; ManyHeads | AC 5 HD 5 Atk 5 Dam 1d6; ManyHeads |
| Six-Headed Hydra | 8 | Six-Headed Hydra | 8 | 8 | AC 5 HD 6 Atk 6 Dam 1d6; ManyHeads | AC 5 HD 6 Atk 6 Dam 1d6; ManyHeads |
| Seven-Headed Hydra | 10 | Seven-Headed Hydra | 10 | 10 | AC 5 HD 7 Atk 7 Dam 1d6; ManyHeads | AC 5 HD 7 Atk 7 Dam 1d6; ManyHeads |
| Eight-Headed Hydra | 11 | Eight-Headed Hydra | 12 | 12 | AC 5 HD 8 Atk 8 Dam 1d6; ManyHeads | AC 5 HD 8 Atk 8 Dam 1d6; ManyHeads |
| Nine-Headed Hydra | 14 | Nine-Headed Hydra | 16 | 14 | AC 5 HD 9 Atk 9 Dam 1d6; ManyHeads | AC 5 HD 9 Atk 9 Dam 1d6; ManyHeads |
| Ten-Headed Hydra | 17 | Ten-Headed Hydra | 17 | 17 | AC 5 HD 10 Atk 10 Dam 1d6; ManyHeads | AC 5 HD 10 Atk 10 Dam 1d6; ManyHeads |
| Eleven-Headed Hydra | 20 | Eleven-Headed Hydra | 21 | 20 | AC 5 HD 11 Atk 11 Dam 1d6; ManyHeads | AC 5 HD 11 Atk 11 Dam 1d6; ManyHeads |
| Twelve-Headed Hydra | 23 | Twelve-Headed Hydra | 23 | 22 | AC 5 HD 12 Atk 12 Dam 1d6; ManyHeads | AC 5 HD 12 Atk 12 Dam 1d6; ManyHeads |
| Very Young White Dragon | 1 | Very Young White Dragon | 4 | 4 | AC 5 HD 2-1 Atk 1 Dam 1d6; Flight (12), Detection (6), ColdBreath, ColdImmunity | AC 2 HD 6 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), ColdBreath |
| Young White Dragon | 2 | Young White Dragon | 7 | 7 | AC 4 HD 3 Atk 1 Dam 1d6; Flight (18), Detection (6), ColdBreath, ColdImmunity | AC 2 HD 6 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), ColdBreath |
| Sub-Adult White Dragon | 6 | Sub-Adult White Dragon | 11 | 11 | AC 4 HD 5 Atk 1 Dam 1d6; Flight (24), Detection (6), Fearlessness, ColdBreath, ColdImmunity | AC 2 HD 6 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), ColdBreath |
| Adult White Dragon | 12 | Adult White Dragon | 13 | 14 | AC 3 HD 7 Atk 1 Dam 1d6; Flight (24), Detection (6), Fearlessness, ColdBreath, ColdImmunity | AC 2 HD 6 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), ColdBreath |
| Old White Dragon | 23 | Old White Dragon | 15 | 16 | AC 3 HD 9 Atk 1 Dam 1d6+2; Flight (24), Detection (6), Fearlessness, Fear (2), ColdBreath, ColdImmunity | AC 2 HD 6 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), ColdBreath |
| Very Old White Dragon | 41 | Very Old White Dragon | 18 | 20 | AC 2 HD 11 Atk 1 Dam 2d6; Flight (24), Detection (6), Fearlessness, Fear (2), ColdBreath, ColdImmunity | AC 2 HD 6 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), ColdBreath |
| Very Young Black Dragon | 1 | Very Young Black Dragon | 4 | 5 | AC 5 HD 2 Atk 1 Dam 1d6; Flight (12), Detection (6), AcidBreath, AcidImmunity | AC 2 HD 7 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), AcidBreath |
| Young Black Dragon | 3 | Young Black Dragon | 8 | 9 | AC 4 HD 4 Atk 1 Dam 1d6; Flight (18), Detection (6), AcidBreath, AcidImmunity | AC 2 HD 7 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), AcidBreath |
| Sub-Adult Black Dragon | 7 | Sub-Adult Black Dragon | 12 | 12 | AC 4 HD 6 Atk 1 Dam 1d6; Flight (24), Detection (6), Fearlessness, AcidBreath, AcidImmunity | AC 2 HD 7 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), AcidBreath |
| Adult Black Dragon | 14 | Adult Black Dragon | 16 | 15 | AC 3 HD 8 Atk 1 Dam 1d6+2; Flight (24), Detection (6), Fearlessness, AcidBreath, AcidImmunity | AC 2 HD 7 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), AcidBreath |
| Old Black Dragon | 28 | Old Black Dragon | 18 | 21 | AC 3 HD 10 Atk 1 Dam 1d6+2; Flight (24), Detection (6), Fearlessness, Fear (2), AcidBreath, AcidImmunity | AC 2 HD 7 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), AcidBreath |
| Very Old Black Dragon | 43 | Very Old Black Dragon | 25 | 24 | AC 2 HD 12 Atk 1 Dam 2d6; Flight (24), Detection (6), Fearlessness, Fear (2), AcidBreath, AcidImmunity | AC 2 HD 7 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), AcidBreath |
| Very Young Green Dragon | 1 | Very Young Green Dragon | 6 | 5 | AC 5 HD 2+1 Atk 1 Dam 1d6; Flight (12), Detection (6), PoisonBreath | AC 2 HD 8 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), PoisonBreath |
| Young Green Dragon | 4 | Young Green Dragon | 10 | 11 | AC 4 HD 5 Atk 1 Dam 1d6; Flight (18), Detection (6), PoisonBreath | AC 2 HD 8 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), PoisonBreath |
| Sub-Adult Green Dragon | 9 | Sub-Adult Green Dragon | 15 | 15 | AC 4 HD 7 Atk 1 Dam 1d6; Flight (24), Detection (6), Fearlessness, PoisonBreath | AC 2 HD 8 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), PoisonBreath |
| Adult Green Dragon | 16 | Adult Green Dragon | 17 | 18 | AC 3 HD 9 Atk 1 Dam 1d6+2; Flight (24), Detection (6), Fearlessness, PoisonBreath | AC 2 HD 8 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), PoisonBreath |
| Old Green Dragon | 31 | Old Green Dragon | 24 | 23 | AC 3 HD 11 Atk 1 Dam 2d6; Flight (24), Detection (6), Fearlessness, Fear (2), PoisonBreath | AC 2 HD 8 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), PoisonBreath |
| Very Old Green Dragon | 52 | Very Old Green Dragon | 28 | 28 | AC 2 HD 13 Atk 1 Dam 2d6; Flight (24), Detection (6), Fearlessness, Fear (2), PoisonBreath | AC 2 HD 8 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), PoisonBreath |
| Very Young Blue Dragon | 1 | Very Young Blue Dragon | 6 | 6 | AC 5 HD 2+2 Atk 1 Dam 1d6; Flight (12), Detection (6), VoltBreath, VoltImmunity | AC 2 HD 9 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), VoltBreath |
| Young Blue Dragon | 4 | Young Blue Dragon | 12 | 12 | AC 4 HD 5+2 Atk 1 Dam 1d6; Flight (18), Detection (6), VoltBreath, VoltImmunity | AC 2 HD 9 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), VoltBreath |
| Sub-Adult Blue Dragon | 11 | Sub-Adult Blue Dragon | 14 | 15 | AC 4 HD 8 Atk 1 Dam 1d6+2; Flight (24), Detection (6), Fearlessness, VoltBreath, VoltImmunity | AC 2 HD 9 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), VoltBreath |
| Adult Blue Dragon | 20 | Adult Blue Dragon | 24 | 22 | AC 3 HD 10 Atk 1 Dam 1d6+2; Flight (24), Detection (6), Fearlessness, VoltBreath, VoltImmunity | AC 2 HD 9 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), VoltBreath |
| Old Blue Dragon | 38 | Old Blue Dragon | 25 | 28 | AC 3 HD 12 Atk 1 Dam 2d6; Flight (24), Detection (6), Fearlessness, Fear (2), VoltBreath, VoltImmunity | AC 2 HD 9 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), VoltBreath |
| Very Old Blue Dragon | 57 | Very Old Blue Dragon | 33 | 33 | AC 2 HD 14 Atk 1 Dam 2d6; Flight (24), Detection (6), Fearlessness, Fear (2), VoltBreath, VoltImmunity | AC 2 HD 9 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), VoltBreath |
| Very Young Red Dragon | 1 | Very Young Red Dragon | 7 | 7 | AC 5 HD 2+3 Atk 1 Dam 1d6; Flight (12), Detection (6), FireBreath, FireImmunity | AC 2 HD 10 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), FireBreath |
| Young Red Dragon | 5 | Young Red Dragon | 12 | 13 | AC 4 HD 6 Atk 1 Dam 1d6; Flight (18), Detection (6), FireBreath, FireImmunity | AC 2 HD 10 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), FireBreath |
| Sub-Adult Red Dragon | 12 | Sub-Adult Red Dragon | 19 | 19 | AC 4 HD 9 Atk 1 Dam 1d6+2; Flight (24), Detection (6), Fearlessness, FireBreath, FireImmunity | AC 2 HD 10 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), FireBreath |
| Adult Red Dragon | 24 | Adult Red Dragon | 27 | 27 | AC 3 HD 11 Atk 1 Dam 2d6; Flight (24), Detection (6), Fearlessness, FireBreath, FireImmunity | AC 2 HD 10 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), FireBreath |
| Old Red Dragon | 41 | Old Red Dragon | 32 | 33 | AC 3 HD 13 Atk 1 Dam 2d6; Flight (24), Detection (6), Fearlessness, Fear (2), FireBreath, FireImmunity | AC 2 HD 10 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), FireBreath |
| Very Old Red Dragon | 72 | Very Old Red Dragon | 38 | 40 | AC 2 HD 15 Atk 1 Dam 3d6; Flight (24), Detection (6), Fearlessness, Fear (2), FireBreath, FireImmunity | AC 2 HD 10 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), FireBreath |
| Very Young Gold Dragon | 4 | Very Young Gold Dragon | 12 | 12 | AC 5 HD 2-1 Atk 1 Dam 1d6; Flight (12), Detection (6), FireBreath, SaveBonus (4), Spells | AC 2 HD 11 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), FireBreath, PoisonBreath, Spells |
| Young Gold Dragon | 6 | Young Gold Dragon | 17 | 20 | AC 4 HD 4 Atk 1 Dam 1d6; Flight (18), Detection (6), FireBreath, SaveBonus (4), Spells | AC 2 HD 11 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), FireBreath, PoisonBreath, Spells |
| Sub-Adult Gold Dragon | 18 | Sub-Adult Gold Dragon | 36 | 40 | AC 4 HD 7 Atk 1 Dam 1d6; Flight (24), Detection (6), Fearlessness, FireBreath, SaveBonus (4), Spells | AC 2 HD 11 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), FireBreath, PoisonBreath, Spells |
| Adult Gold Dragon | 38 | Adult Gold Dragon | 47 | 50 | AC 3 HD 10 Atk 1 Dam 1d6+2; Flight (24), Detection (6), Fearlessness, FireBreath, SaveBonus (4), Spells | AC 2 HD 11 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), FireBreath, PoisonBreath, Spells |
| Old Gold Dragon | 77 | Old Gold Dragon | 55 | 60 | AC 3 HD 13 Atk 1 Dam 2d6; Flight (24), Detection (6), Fearlessness, Fear (2), FireBreath, SaveBonus (4), Spells | AC 2 HD 11 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), FireBreath, PoisonBreath, Spells |
| Very Old Gold Dragon | 111 | Very Old Gold Dragon | 57 | 65 | AC 2 HD 16 Atk 1 Dam 3d6; Flight (24), Detection (6), Fearlessness, Fear (2), FireBreath, SaveBonus (4), Spells | AC 2 HD 11 Atk 2 Dam 2d6; Flight (24), Detection (15), Fear (2), FireBreath, PoisonBreath, Spells |
