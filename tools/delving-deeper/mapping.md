# Delving Deeper -> Arena monster mapping

This is the proposal for turning every monster in the Delving Deeper
reference rules (Section III, *Monsters*) into rows of
`MonsterDatabase-DelvingDeeper.csv`. It is rendered by `generate.py` from
`mapping.json` + `tables.json`, so what you see here is exactly what the CSV
will contain. Edit `mapping.json` and re-run `python3 generate.py --all`.

## Derivation rules

Columns: `Monster,Number,AC,MV,HD,Lair%,Treas,Atk,Dam,Align,Type,EHD,HDD,Env,Source,Special`.

* **Stats source.** Table 3.1 (summary) unless a detail table exists: dragons
  (Tables 3.4-3.9), giants (3.10), horses (3.11), rocs (3.12). Where the two
  disagree the detail table wins (e.g. Destrier MV 15, Fire Elemental HD).
* **Number.** DD "a-b" ranges become Arena dice: prefer an expression with no
  modifier (2-8 -> 2d4, 3-12 -> 3d4, 10-80 -> 10d8), else the d6 form with the
  smallest modifier (3-8 -> 1d6+2, 4-14 -> 2d6+2, 6-21 -> 3d6+3, 1-11 -> 2d6-1),
  else the fewest dice (2-9 -> 1d8+1, 2-5 -> 1d4+1). "n/a" (horses) -> 1.
  Number appearing (wandering) is used, not number in lair.
* **AC.** Split ACs are hit-location or facing values; the one a melee
  attacker faces is used, following the master file (Salamander 5 not 3,
  Giant Squid 7 not 3, Giant Centipede 3, Triceratops 2, Stegosaurus 5).
  "7*" (barded) -> 7. The unused value is recorded in NOTES.md.
* **MV.** First value of a split move; the second value goes into Special as
  `Flight (n)` / `Swimming (n)` / `WebMove (n)` following MonsterDatabase.csv.
  "-/n" fliers keep n as MV (master Air Elemental idiom); "-/n" swimmers get
  MV 0 (master aquatic idiom). Burrowing/climbing/wall-crawling secondaries
  have no master idiom and are listed in NOTES.md instead.
* **HD.** As written (`1/2`, `3+1`, `1-1` all parse). A *range* of HD
  (giant beetles 2-7, pterodactyls 2-7, giant fish 4-9, hydras 5-12,
  elementals 8/12/16) becomes one row per value, named
  "Two Hit Dice Giant Beetle", "Five-Headed Hydra",
  "Eight Hit Dice Air Elemental", etc.
* **Lair%.** "n/a" -> `-`. **Treas.** First character; `*` (coins carried) and
  "n/a" -> `-`; A1/A2/A3 -> A; E* -> E. **Align.** First listed ("C, N" -> C,
  "L, N" -> L, "Any" -> N).
* **Atk / Dam.** From the *Explanation of Monsters* prose; single attack roll
  and 1d6 when unstated (DD Combat, *Damage*). Prose ranges convert like
  Number. Multiple attack rolls (centaur 2, chimera 3, gothrog 2, hydra
  heads, octopus/squid/kraken "1-6 rolls" -> 4) become Atk.
  The "exceeds the number required by 4 or more, or a 20" bigger-damage
  pattern is *not* modelled; base damage is used and every case is listed
  in NOTES.md.
* **Type.** Same letters as MonsterDatabase.csv: A animal (normal, giant,
  prehistoric, aquatic), B beast/monster (fantastic creatures, lycanthropes,
  golems, dragons), F faerie/sylvan and noble creatures (dwarf, elf, pixie,
  pegasus, roc, treant), H humanoid (kobold to giant), M men,
  S slime/mold/ooze (auto-adds Slime), U undead (auto-adds Undead),
  X extraplanar (elementals, djinni, efreeti, invisible stalker).
* **EHD** `?` (Arena computes it). **HDD** HD as a decimal, +0.3 per bonus
  hit point (`3+1` -> 3.3, `1-1` -> 0.7, `1/2` -> 0.5), as in the master file.
  **Env** D dungeon, W wilderness, U underwater, X extraplanar (as master).
  **Source** `DD`.
* **Special.** Exact `SpecialType` enum names, `Name (n)` for parameters,
  plus the three master-file movement words (`Flight`, `Swimming`,
  `WebMove`) which Arena silently ignores. Parameter meanings used:
  `Poison (n)` / `Charm (n)` = target's save modifier; `Fear (n)` = enemies
  of HD <= n must save or flee; `MagicToHit (n)` = weapon plus needed;
  `ChopResistance (n)` = half damage from weapons below magic level n
  (0 = all); `Regeneration (n)` = hp per round; `BloodDrain (n)` = 1d(n)
  per round while attached; `EnergyDrain (n)` = levels per hit;
  `Whirlwind (n)` = width; `FireBreath (n)` = n dice / cone length;
  `SaveBonus (n)`; `HitBonus (n)`; `Spells (n)` = nth-level wizard
  (bare `Spells` for the Gold Dragon and Titan, which Monster.java
  special-cases by name); `Detection (n)` = sees invisible.
  Names Arena only implements as *conditions* (Sleep, Webs, Death, Hold,
  Disintegration) are listed where DD clearly describes the ability, but are
  inert; see NOTES.md.
* **Names.** Natural singular, Arena style. DD spellings kept where DD's
  monster is its own thing (Manticora, Gothrog, Thull, Wight Ape,
  Sabre-Toothed Tiger); "Golden Dragon" becomes "Gold Dragon" so
  Monster.java's Gold Dragon spell handling applies.
* **Dragons.** DD ages Hatchling / Young / Adult / Mature / Old / Ancient map
  in order onto Arena's Very Young / Young / Sub-Adult / Adult / Old /
  Very Old. Each age is a row with that age's AC, MV, HD and melee damage.
  Specials: `Flight (n)`, breath type, immunity, `Fear (2)` from DD Mature
  up ("greater dragons" force normal-types to check morale; Combat,
  *Morale*), Gold adds `SaveBonus (4)` and `Spells`. Hatchlings have no
  treasure (*Dragon Treasure*).

## Master-file vocabulary deliberately not used

MonsterDatabase.csv uses many Special names that are not in `SpecialType`
(Stealth, Disease, Lycanthropy, Spawn, Camouflage, Bravery, Cowardice,
LightSensitivity, Splitting, GasForm, Creation, Tracking, Leaping, Jet,
InkCloud, WeatherControl, DimensionDoor, Grappling, LandWeakness, Undying).
Arena drops them silently. Apart from the three movement words above, this
file does not use them; the corresponding DD abilities are recorded per
monster in NOTES.md so they can be added if Dan implements them.

## Mapping table

Grouped entries (dragons, HD ranges, hydras, elementals) are shown once with
the row count; the Special column shows the pattern shared by every row.

| DD entry | Arena row(s) | Num | AC | MV | HD | Lair | Tr | Atk | Dam | Al | Ty | Env | Special | Rationale |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Androids | Android | 1d8 | 9 | 12 | 2 | 15 | A | 1 | 1d6 | N | M | D | Spells (2) | Align 'Any' -> N. 'Mind powers equivalent to magic use of up to 4th level' on d6-2 per android (2/3 have them, mean level 2.5) -> Spells (2) as a typical individual. |
| Ants, giant | Giant Ant | 2d6 | 3 | 18 | 2 | 10 | C | 1 | 1d6 | N | A | D | - | Unmapped: Secondary move 3 is burrowing (no Arena code). Never flee the nest while the queen lives (lair-only). |
| Apes | Ape | 1d8 | 6 | 12 | 4+1 | - | - | 1 | 1d6+1 | N | A | W | - | Unmapped: Secondary move 12 is climbing (no Arena code). |
| Basilisks | Basilisk | 1d6 | 4 | 6 | 6+1 | 40 | F | 1 | 1d6 | C | B | D | PetrifyingGaze, Petrification | Gaze or touch petrifies (save vs petrification): same pair as master Basilisk. |
| Bats | Bat | 10d8 | 8 | 3 | 1/2 | 15 | - | 0 | 0 | N | A | D | Flight (12) | 'Mostly harmless': Atk 0 / Dam 0 as master does for Shrieker. Unmapped: Startled colony obscures sight, drops torches, interrupts spellcasting. |
| Bats, giant | Giant Bat | 1d8 | 7 | 3 | 4 | 15 | C | 1 | 1d6 | N | A | D | Flight (15) | Unmapped: Surprise on 3+ on d6 (master would write Stealth (n), not an enum name). Shriek makes normal-types cover ears for one turn. |
| Bears | Bear | 1d6 | 6 | 12 | 5+5 | - | - | 1 | 1d6+2 | N | A | W | - | CRIT-DAMAGE PATTERN: 3-8 normally, 4-14 on exceeds-by-4 / natural 20. |
| Beetles, giant | Two Hit Dice Giant Beetle ... Seven Hit Dice Giant Beetle (6 rows) | 1d12 | 3 | 9 | 2..7 | - | - | 1 | 1d6 | N | A | D | - | HD 2-7 is a range: one row per HD value. No damage stated -> default 1d6 for every size. Unmapped: Secondary move 6 is tunnelling through soft earth. |
| Black pudding | Black Pudding | 1 | 7 | 3 | 10 | - | - | 1 | 3d6 | N | S | D | WoodEating, MetalEating, VoltImmunity, ColdImmunity, ChopImmunity | Dissolves wood and metal armor -> WoodEating, MetalEating. Invulnerable to cold -> ColdImmunity. Lightning and slashing divide it harmlessly -> VoltImmunity, ChopImmunity (master Black Pudding uses the same set). Unmapped: Splitting into smaller puddings (master writes Splitting, not an enum name). Susceptible to fire (no vulnerability stated beyond being harmable). |
| Boars | Boar | 1d12 | 7 | 15 | 1+2 | - | - | 1 | 1d6 | N | A | W | - | Unmapped: One more attack roll after being reduced to 0 hp. |
| Boars, giant | Giant Boar | 1d8 | 6 | 12 | 7 | - | - | 1 | 2d6 | N | A | W | Fearlessness | 'Will never retreat' -> Fearlessness. Unmapped: One more attack roll after being reduced to 0 hp. |
| Cave bears | Cave Bear | 1d2 | 6 | 12 | 6+6 | - | - | 1 | 2d6-1 | N | A | W | - | CRIT-DAMAGE PATTERN: 1-11 normally, 3-18 on exceeds-by-4 / natural 20. Unmapped: One more attack roll after being reduced to 0 hp. |
| Cavemen | Caveman | 2d6 | 9 | 12 | 2 | 15 | C | 1 | 1d6 | N | M | W | - | Unmapped: -1 morale (master writes Cowardice, not an enum name). |
| Centaurs | Centaur | 2d4 | 6 | 18 | 4 | 5 | A | 2 | 1d6 | L | F | W | - | Two attack rolls (weapon and hooves) -> Atk 2. Align 'L, N' -> L. Treasure A1 -> A. |
| Centipedes, giant | Giant Centipede | 1d6 | 3 | 12 | 3+1 | 60 | B | 1 | 1d6 | N | A | D | Paralysis | AC 3/7 (armored head / soft body) -> 3, the head a fighter faces. Bite paralyses with a save -> Paralysis. Unmapped: Split AC: body is AC 7 (Arena has one AC). Moves on walls and ceilings at full speed. |
| Centipedes, large | Large Centipede | 2d12 | 9 | 6 | 1/2 | - | - | 1 | 1d6 | N | A | D | Paralysis | Paralysis save is at +4 for large centipedes; Arena's Paralysis takes no save-modifier parameter (only Poison does), so the +4 is lost. No damage stated -> default 1d6 (master gives its tiny centipede Dam 0). |
| Chimeras | Chimera | 1d4 | 4 | 12 | 9 | 50 | F | 3 | 1d6 | C | B | D | Flight (18), FireBreath (3) | Three heads -> Atk 3. 6" cone of fire for 3-18 -> FireBreath (3) (Arena: n dice of damage, cone length n). Same as master Chimera. |
| Cockatrices | Cockatrice | 1d8 | 6 | 9 | 5 | 35 | D | 1 | 1d6 | C | B | D | Flight (18), Petrification | Touch petrifies (save vs petrification) -> Petrification on hit. |
| Crabs, giant | Giant Crab | 3d4 | 3 | 6 | 3 | - | - | 1 | 1d6 | N | A | U | - | CRIT-DAMAGE PATTERN: 1-6 (default) normally, 1-11 on exceeds-by-4 / natural 20. |
| Crocodiles | Crocodile | 2d6 | 6 | 9 | 3 | 20 | - | 1 | 1d6 | N | A | U | Swimming (15) | Exceeds-by-4 trigger: exceeds-by-4: drags victim into the water and drowns it. Unmapped: Hard to spot half-submerged; often attacks by surprise. |
| Crocodiles, giant | Giant Crocodile | 1d6 | 5 | 9 | 7 | 20 | - | 1 | 2d6 | N | A | U | Swimming (15), Swallowing | Swallows man-sized victim whole on exceeds-by-4 -> Swallowing (Arena triggers it on a total attack roll of 25+, the closest analogue). Exceeds-by-4 trigger: exceeds-by-4: swallow whole (mapped to Swallowing). Unmapped: Overturns boats and rafts; can be rammed by ships. |
| Cyborgs | Cyborg | 2d4 | 5 | 9 | 3+3 | 15 | G | 1 | 1d6+2 | C | M | D | Fearlessness | 'Need never check morale' -> Fearlessness. Align 'C, N' -> C. Unmapped: Never give up a pursuit while quarry in sight. |
| Cyclopes | Cyclops | 1d4 | 2 | 15 | 16 | 30 | E | 1 | 3d6+3 | N | H | W | RockHurling, HitBonus (-2) | Hurls rocks up to 20" for 2-12 -> RockHurling (Arena: 2d6 rock). Poor depth perception -2 on attack rolls -> HitBonus (-2). Treasure E* -> E. |
| Dinosaurs, Brontosaurs | Brontosaurus | 1d6 | 5 | 6 | 32 | - | - | 1 | 3d6 | N | A | W | - |  |
| Dinosaurs, Deinonychus | Deinonychus | 1d6 | 5 | 21 | 4 | - | - | 1 | 1d6 | N | A | W | - | Unmapped: Stalks prey and never gives up pursuit while prey in sight. |
| Dinosaurs, Mosasaur | Mosasaurus | 1d4 | 5 | 3 | 14 | - | - | 1 | 3d6 | N | A | U | Swimming (15), Swallowing | Exceeds-by-4 trigger: exceeds-by-4 / natural 20: swallow whole (mapped to Swallowing). |
| Dinosaurs, Pterodactyls | Two Hit Dice Pterodactyl ... Seven Hit Dice Pterodactyl (6 rows) | 1d8 | 5 | 3 | 2..7 | - | - | 1 | 1d6 | N | A | W | Flight (12) | HD 2-7 is a range: one row per HD value. No damage stated -> default 1d6. |
| Dinosaurs, Stegosaurs | Stegosaurus | 2d4 | 5 | 6 | 8 | - | - | 1 | 1d6+2 | N | A | W | - | AC 2/5: the plates give AC 2 only against attacks not from the flank; a surrounding party mostly flanks it, so 5 is used. Damage 3-8 normally. Unmapped: Split AC: AC 2 against attacks other than from the flank (Arena has one AC). Tail spikes do 2-12 to flank or rear attackers. |
| Dinosaurs, Triceratops | Triceratops | 2d4 | 2 | 9 | 16 | - | - | 1 | 2d6 | N | A | W | - | AC 2/5: frill and horns give AC 2 from the front; it charges head-on, so 2 is used. Unmapped: Split AC: AC 5 from other facings (Arena has one AC). Charge does 4-24 instead of 2-12. |
| Dinosaurs, Tyrannosaurus Rexes | Tyrannosaurus Rex | 1d2 | 5 | 15 | 20 | - | - | 1 | 4d6 | N | A | W | Swallowing | Exceeds-by-4 trigger: exceeds-by-4 / natural 20: swallow whole (mapped to Swallowing). |
| Djinni | Djinni | 1 | 6 | 9 | 7+1 | - | - | 1 | 2d6-1 | N | X | X | Flight (24), Invisibility, Illusion, Whirlwind (2) | 1-11 damage -> 2d6-1 (as master Djinni). Becomes invisible -> Invisibility; phantasm-like illusions -> Illusion; whirlwind 2" wide -> Whirlwind (2) (parameter is width; master uses 1). Env X for extraplanar as in master. Unmapped: Gaseous form (master writes GasForm). Object creation (master writes Creation). |
| Dogs | Dog | 4d4 | 7 | 15 | 1 | - | - | 1 | 1d6 | N | A | W | - |  |
| Doppelgangers | Doppelganger | 1d6 | 5 | 9 | 4 | 25 | E | 1 | 1d6 | C | B | D | Polymorphism, SaveBonus (6) | Shape change -> Polymorphism. Saves as a 10th-level fighter -> SaveBonus (6), master's idiom for the identical OD&D text. Align 'C, N' -> C. Unmapped: Immune to sleep and charm. |
| Dragon turtles | Dragon Turtle | 1d4 | 2 | 3 | 12 | 60 | H | 1 | 1d6 | N | B | U | Swimming (9), SteamBreath | Name ends in 'Dragon Turtle' so Arena adds the Dragon special itself (breath = hit points, random age category for hp). 9"x3" cone of scalding steam 'as a dragon's breath weapon' -> SteamBreath. No melee damage stated -> default 1d6. Unmapped: 50% chance to capsize a ship it surfaces under. |
| Dragons, Black | Very Young Black Dragon ... Very Old Black Dragon (6 rows) | 1d4 | 5/4/3/2 | 6 | 2..12 | 60 | -/H | 1 | 1d6/1d6+2/2d6 | C | B | D | Flight (12/18/24 by age), AcidBreath, AcidImmunity, Fear (2) from Adult up | Line of acid -> AcidBreath; invulnerable to acid -> AcidImmunity. Unmapped: Swims and breathes underwater indefinitely (no rate given). |
| Dragons, Blue | Very Young Blue Dragon ... Very Old Blue Dragon (6 rows) | 1d4 | 5/4/3/2 | 6 | 2+2..14 | 60 | -/H | 1 | 1d6/1d6+2/2d6 | C | B | D | Flight (12/18/24 by age), VoltBreath, VoltImmunity, Fear (2) from Adult up | Line of lightning -> VoltBreath; invulnerable to lightning -> VoltImmunity. Unmapped: Buries itself in sand for ambush. |
| Dragons, Golden | Very Young Gold Dragon ... Very Old Gold Dragon (6 rows) | 1d4 | 5/4/3/2 | 6 | 2-1..16 | 60 | -/H | 1 | 1d6/1d6+2/2d6/3d6 | L | B | D | Flight (12/18/24 by age), FireBreath, SaveBonus (4), Spells, Fear (2) from Adult up | Named 'Gold Dragon' (Arena's spelling) so Monster.java's Gold Dragon spell handling applies: bare 'Spells' makes Arena add two spells per level up to the age category, which tracks DD's 'as many spells as hit dice, up to 3rd level (6th for ancient goldens)' closely enough. Saves +4 vs magic -> SaveBonus (4). Sonic breath has no SpecialType: FireBreath used as a plain-damage stand-in (see NOTES). Unmapped: Breath is sound, not fire (also damages structures). Cannot be subdued; polymorphs into human form. |
| Dragons, Green | Very Young Green Dragon ... Very Old Green Dragon (6 rows) | 1d4 | 5/4/3/2 | 6 | 2+1..13 | 60 | -/H | 1 | 1d6/1d6+2/2d6 | C | B | D | Flight (12/18/24 by age), PoisonBreath, Fear (2) from Adult up | Cone of chlorine -> PoisonBreath. Unmapped: Immune to poison (no PoisonImmunity in SpecialType). |
| Dragons, Red | Very Young Red Dragon ... Very Old Red Dragon (6 rows) | 1d4 | 5/4/3/2 | 6 | 2+3..15 | 60 | -/H | 1 | 1d6/1d6+2/2d6/3d6 | C | B | D | Flight (12/18/24 by age), FireBreath, FireImmunity, Fear (2) from Adult up | Cone of fire -> FireBreath; invulnerable to fire -> FireImmunity. |
| Dragons, White | Very Young White Dragon ... Very Old White Dragon (6 rows) | 1d4 | 5/4/3/2 | 6 | 2-1..11 | 60 | -/H | 1 | 1d6/1d6+2/2d6 | C | B | D | Flight (12/18/24 by age), ColdBreath, ColdImmunity, Fear (2) from Adult up | Cone of cold -> ColdBreath; invulnerable to cold -> ColdImmunity. Unmapped: Swims and tunnels through snow and ice (no rates given). |
| Dryads | Dryad | 1d6 | 5 | 12 | 2 | 20 | D | 1 | 1d6 | L | F | W | Charm (-2) | Charm with save vs spells at -2 -> Charm (-2) (parameter is the target's save modifier), identical to master. Align 'L, N' -> L. Unmapped: Non-violent; bound within 24" of its tree. |
| Dwarfs | Dwarf | 2d6 | 4 | 9 | 1 | 50 | G | 1 | 1d6 | L | F | W | DodgeGiants | Ogres, trolls and giants do half damage to dwarfs -> DodgeGiants (Arena: -4 to hit by H-type monsters of 4+ HD), the master's code for the same OD&D rule. No save bonus in DD, so master's SaveBonus (4) is not carried over. Unmapped: Half damage from ogres/trolls/giants is modelled as a to-hit penalty, not a damage halving. |
| Efreeti | Efreeti | 1 | 4 | 9 | 10 | - | - | 1 | 2d6 | C | X | X | Flight (24), Invisibility, Illusion, WallOfFire | Flies, invisibility, illusions, wall of fire -> Flight, Invisibility, Illusion, WallOfFire (all in master Efreeti). Unmapped: 'Become incendiaries' (immolation of self; no fire immunity stated). Object creation (master writes Creation). |
| Elemental, Air | Eight Hit Dice Air Elemental ... Sixteen Hit Dice Air Elemental (3 rows) | 1 | 3 | 36 | 8..16 | - | - | 1 | 1d6+1 | N | X | X | Flight (36), Whirlwind (3) | HD 8/12/16 -> three rows. Move '-/36': flight only, so MV 36 plus Flight (36) as master does. 2-7 damage -> 1d6+1. Whirlwind 3" wide at base -> Whirlwind (3), as master. DD says nothing about needing magic weapons, so master's MagicToHit (2) is not carried over. Unmapped: +2 to hit vs aerial opponents. Whirlwind height grows with HD. |
| Elemental, Earth | Eight Hit Dice Earth Elemental ... Sixteen Hit Dice Earth Elemental (3 rows) | 1 | 3 | 6 | 8..16 | - | - | 1 | 3d6 | N | X | X | - | 3-18 vs opponents on solid ground -> 3d6 (2-12 vs airborne not modelled). Unmapped: Secondary move 6 is through earth; cannot cross water; move earth drives it back for 6-36. |
| Elemental, Fire | Eight Hit Dice Fire Elemental ... Sixteen Hit Dice Fire Elemental (3 rows) | 1 | 3 | 12 | 8..16 | - | - | 1 | 2d6 | N | X | X | - | Summary table says HD 11+3 but the Explanation of Monsters gives 8/12/16 for all elementals; 8/12/16 used (see NOTES). 2-12 damage -> 2d6 (2-7 vs fire creatures not modelled). No fire immunity is stated, so none added. Unmapped: Ignites inflammables; cannot cross water. |
| Elemental, Water | Eight Hit Dice Water Elemental ... Sixteen Hit Dice Water Elemental (3 rows) | 1 | 3 | 6 | 8..16 | - | - | 1 | 2d6 | N | X | X | Swimming (18) | 2-12 in water, 1-6 on land -> 2d6 (the in-water figure, as master). Unmapped: Overturns boats; must stay within 6" of water. |
| Elves | Elf | 2d6 | 7 | 12 | 1 | 25 | E | 1 | 1d6 | L | F | W | - | Align 'L, N' -> L. Unmapped: +1 damage with magic weapons. Move silently / near-invisibly in woods (master writes Camouflage). Leader-types with fighter/magic-user levels. |
| Fish, giant | Four Hit Dice Giant Fish ... Nine Hit Dice Giant Fish (6 rows) | 2d6 | 5 | 0 | 4..9 | - | - | 1 | 1d6 | N | A | U | Swimming (30) | HD 4-9 is a range: one row per HD value. Move '-/30': MV 0 plus Swimming (30), the master idiom for purely aquatic creatures. |
| Gargoyles | Gargoyle | 1d10 | 6 | 9 | 4 | 25 | C | 1 | 1d6 | C | B | D | Flight (15), MagicToHit (1) | 'Normal weapons do them no harm' -> MagicToHit (1), as master. Unmapped: Indistinguishable from statues; 75% hostile. |
| Gelatinous cube | Gelatinous Cube | 1 | 8 | 6 | 4 | - | - | 1 | 1d6 | N | S | D | Paralysis, VoltImmunity, ColdImmunity | Contact paralyses (save) then 1-6/turn -> Paralysis, Dam 1d6. Invulnerable to cold and lightning -> ColdImmunity, VoltImmunity. Type S adds Slime (non-sentient, so immune to mental attacks). Treasure '*' (absorbed items) -> '-'. Unmapped: Immune to fear, paralysis and polymorph (fear/paralysis partly covered by Slime being non-sentient). |
| Ghouls | Ghoul | 1d12 | 7 | 9 | 2 | 20 | B | 1 | 1d6 | C | U | D | Paralysis | Touch paralyses normal man-types 1 turn -> Paralysis. Type U adds Undead. Unmapped: -2 attack and morale in daylight. Elves immune to the paralysis. Slain man-types rise as ghouls (master writes Spawn). |
| Giants, Hill | Hill Giant | 1d8 | 4 | 12 | 8 | 30 | E | 1 | 2d6 | C | H | D | - | Stats from Table 3.10. DD does not say hill giants throw rocks, so master's RockHurling is not added (see NOTES). |
| Giants, Stone | Stone Giant | 1d8 | 2 | 12 | 9 | 30 | E | 1 | 2d6 | N | H | D | RockHurling | Hurls rocks for 3-18 -> RockHurling (Arena's rock does 2d6). |
| Giants, Frost | Frost Giant | 1d8 | 4 | 12 | 10+1 | 30 | E | 1 | 2d6+1 | C | H | D | ColdImmunity | Invulnerable to cold -> ColdImmunity. 3-13 -> 2d6+1 (as master). |
| Giants, Fire | Fire Giant | 1d8 | 3 | 12 | 11+3 | 30 | E | 1 | 2d6+2 | C | H | D | FireImmunity | Invulnerable to fire -> FireImmunity. 4-14 -> 2d6+2 (as master). |
| Giants, Cloud | Cloud Giant | 1d8 | 3 | 15 | 12+2 | 30 | E | 1 | 3d6 | N | H | D | Detection | Keen smell, rarely surprised -> Detection (master's code for the same OD&D text). |
| Giants, Storm | Storm Giant | 1d8 | 2 | 15 | 15 | 30 | E | 1 | 3d6+3 | N | H | D | RockHurling, VoltImmunity | Hurls rocks -> RockHurling. Invulnerable to lightning -> VoltImmunity. 6-21 -> 3d6+3 (as master). Unmapped: Weather control (master writes WeatherControl). Lightning strike for 8-48 in thunderstorm conditions. |
| Gnolls | Gnoll | 2d5 | 6 | 9 | 2 | 30 | D | 1 | 1d6 | C | H | D | - | Number 2-10 -> 2d5. Unmapped: +2 morale (master writes Bravery (2)). |
| Gnomes | Gnome | 2d6 | 6 | 9 | 1 | 60 | C | 1 | 1d6 | L | F | W | - | Align 'L, N' -> L. |
| Goblins | Goblin | 2d10 | 7 | 9 | 1-1 | 50 | - | 1 | 1d6 | C | H | D | - | Treasure '*' (1-6 gp each) -> '-'. Unmapped: -1 attack and morale in full daylight (master writes LightSensitivity). |
| Golems, Clay | Clay Golem | 1 | 2 | 6 | 12 | - | - | 1 | 2d6 | N | B | D | MagicToHit (1) | Only harmed by magic weapons -> MagicToHit (1). Name ends in Golem so Arena adds Golem. DD lists spells that do affect it, so master's MagicImmunity is not added. Unmapped: Hasted for three turns after one turn of combat. Disintegrate slows it; move earth drives it back for 6-36. Its wounds need a 9th-level cleric to cure. |
| Golems, Flesh | Flesh Golem | 1 | 9 | 9 | 9 | - | - | 1 | 2d6 | N | B | D | MagicToHit (1) | Only harmed by magic weapons -> MagicToHit (1). Cold/fire slow it and lightning heals it, so no MagicImmunity. Unmapped: Slowed by cold and fire spells; healed by lightning. |
| Gorgons | Gorgon | 1d4 | 3 | 12 | 8 | 50 | E | 1 | 1d6 | C | B | D | PetrifyingBreath | 6"x2" petrifying breath thrice per day -> PetrifyingBreath (as master). No melee damage stated -> 1d6. |
| Gothrogs | Gothrog | 1d6 | 3 | 9 | 10 | 25 | F | 2 | 2d6 | C | B | D | Flight (15), MagicToHit (1), MagicResistance (75), FireImmunity, Immolation, Fearlessness | DD's balrog. Sword and whip on two targets for 2-12 each -> Atk 2, Dam 2d6. Fire and normal weapons cannot harm -> FireImmunity, MagicToHit (1). 75% spells fail -> MagicResistance (75). Whip-drag-and-immolate for 2-12 -> Immolation (master Balrog idiom). Never checks morale -> Fearlessness. Unmapped: +2 to hit when using a single weapon; sword alone does 3-18. Cannot be subdued. |
| Gray ooze | Gray Ooze | 1 | 9 | 3 | 3 | - | - | 1 | 2d6 | N | S | D | MetalEating, FireImmunity, ColdImmunity | Dissolves metal armor -> MetalEating; impervious to cold and fire -> ColdImmunity, FireImmunity (identical to master). |
| Green slime | Green Slime | 1 | 9 | 0 | 3 | - | - | 1 | 0 | N | S | D | FleshEating, WoodEating, MetalEating, VoltImmunity, ChopImmunity | Eats flesh, wood and metal -> FleshEating, WoodEating, MetalEating; impervious to lightning and blows -> VoltImmunity, ChopImmunity. Dam 0 because FleshEating carries the effect (same as master). Move 'n/a' -> 0. |
| Griffons | Griffon | 1d8 | 4 | 12 | 7 | 10 | E | 1 | 1d6 | N | F | W | Flight (30) |  |
| Halflings | Halfling | 2d4 | 7 | 9 | 1 | 70 | B | 1 | 1d6 | L | F | W | - | Align 'L, N' -> L. Unmapped: +3 to hit with hurled missiles. Move silently and hide superbly. |
| Hippogriffs | Hippogriff | 1d8 | 6 | 18 | 3+1 | - | - | 1 | 1d6 | N | F | W | Flight (36) | Unmapped: Never checks morale when defending its nest. |
| Hobgoblins | Hobgoblin | 2d6 | 5 | 9 | 1+1 | 30 | D | 1 | 1d6 | C | H | D | - | Unmapped: +1 morale except in daylight, where -1 to hit (master writes Bravery (1)). |
| Horses, Destrier | Destrier | 1 | 7 | 15 | 2+4 | - | - | 1 | 1d6 | N | A | W | - | Stats from Table 3.11 (MV 15 there, 12 in the summary; the detail table wins). AC 7* (4 if barded) -> 7. 'Number' n/a -> 1. |
| Horses, Draft horse | Draft Horse | 1 | 7 | 12 | 2+1 | - | - | 0 | 0 | N | A | W | - | 'Only warhorses and destriers will attack' -> Atk 0 / Dam 0. |
| Horses, Mule | Mule | 1 | 7 | 12 | 2 | - | - | 0 | 0 | N | A | W | - | Does not attack -> Atk 0 / Dam 0. |
| Horses, Riding horse | Riding Horse | 1 | 7 | 24 | 2 | - | - | 0 | 0 | N | A | W | - | Does not attack -> Atk 0 / Dam 0. |
| Horses, War horse | War Horse | 1 | 7 | 18 | 2+2 | - | - | 1 | 1d6 | N | A | W | - | AC 7* (4 if barded) -> 7. |
| Hydras | Five-Headed Hydra ... Twelve-Headed Hydra (8 rows) | 1d2 | 5 | 12 | 5..12 | 25 | B | = heads | 1d6 | N | B | D | ManyHeads | HD 5-12, one head per HD, one attack roll per head -> one row per HD, Atk = heads, ManyHeads (Arena's hydra idiom: max hit points, heads lost as damage accrues). Unmapped: Heads attack as a fighter rather than as a monster. |
| Invisible stalker | Invisible Stalker | 1 | 2 | 12 | 8 | - | - | 1 | 1d6 | N | X | X | Flight (12), Invisibility | Move '-/12': flight only, so MV 12 plus Flight (12). Unmapped: Faultless tracker (master writes Tracking). |
| Juggernaut | Juggernaut | 1 | 2 | 9 | 37 | - | - | 1 | 5d6 | N | B | D | MagicToHit (3), MagicImmunity, Fearlessness, Death, Hold | Only harmed by +3 weapons -> MagicToHit (3). 'Impervious to most magical attacks' -> MagicImmunity (closest code). Never checks morale -> Fearlessness. The jewel's slaying spell and improved hold person each turn -> Death and Hold: both are SpecialType names, but Monster.java only implements them as conditions, not as monster attacks, so they are documentation only (see NOTES). Unmapped: Slaying spell each turn (Death listed but inert). Improved hold person on 2-12 man-types at -2, or one at -6 (Hold listed but inert). Crushes anything in its path; cannot be subdued. |
| Kobolds | Kobold | 2d10 | 7 | 6 | 1/2 | 50 | - | 1 | 1d6 | C | H | D | Swimming (9) | Align 'C, N' -> C. Treasure '*' -> '-'. Unmapped: -1 morale unless defending lair at 3:1 odds. |
| Leeches, giant | Giant Leech | 2d6 | 8 | 3 | 2 | - | - | 1 | 1d6 | N | A | U | Swimming (6), EnergyDrain (1) | Attaches and drains one experience level the turn after attaching and every other turn after -> EnergyDrain (1) per hit is the closest code (master uses BloodDrain because OD&D leeches drain hp, but DD's drain levels). Unmapped: Attachment cadence (drain every other turn, not every hit). |
| Lions | Lion | 1d6 | 6 | 12 | 5+2 | 25 | - | 1 | 1d6+1 | N | A | W | - | CRIT-DAMAGE PATTERN: 2-7 normally, 2-12 on exceeds-by-4 / natural 20. Unmapped: Stalks to attack by surprise (master writes Stealth (2)). |
| Lions, spotted | Spotted Lion | 2d4 | 5 | 12 | 6+2 | 25 | - | 1 | 1d6+2 | N | A | W | - | CRIT-DAMAGE PATTERN: 3-8 normally, 4-14 on exceeds-by-4 / natural 20. |
| Living statues, Iron | Iron Living Statue | 1 | 2 | 6 | 18 | - | - | 1 | 4d6 | N | B | D | Golem, MagicToHit (3), PoisonBreath (1) | Golem added explicitly (name does not end in Golem) for construct behaviour. Only +3 weapons harm it -> MagicToHit (3). 1" cloud of poison gas -> PoisonBreath (1), master Iron Golem idiom. Lightning slows and fire heals it, so no MagicImmunity. Unmapped: Slowed by lightning; healed by fire. |
| Living statues, Stone | Stone Living Statue | 1 | 5 | 6 | 14 | - | - | 1 | 3d6 | N | B | D | Golem, MagicToHit (2), Slowing | Golem added explicitly. Slows one target per turn -> Slowing (master Stone Golem idiom). Only +2 weapons or stone-affecting magic harm it -> MagicToHit (2); not MagicImmunity because stone-affecting spells work. Unmapped: Slowed by cold and fire; healed by stone to flesh. |
| Lizards, giant | Giant Lizard | 1d6 | 5 | 15 | 3+1 | 60 | - | 1 | 1d6 | N | A | D | - | Exceeds-by-4 trigger: natural 20: bite clamps on and does automatic damage each turn. Unmapped: Superb camouflage (master writes Camouflage). |
| Lizards, large | Large Lizard | 1d6 | 8 | 12 | 1/2 | 60 | - | 1 | 1d6 | N | A | D | - | Unmapped: Superb camouflage. |
| Lizardmen | Lizardman | 2d4 | 6 | 6 | 2+1 | 40 | D | 1 | 1d6 | C | H | D | Swimming (12) | Align 'C, N' -> C. |
| Lycanthropes, Werebears | Werebear | 1d10 | 3 | 9 | 6 | 15 | C | 1 | 1d6 | L | B | D | SilverToHit | Only silvered or magic weapons harm -> SilverToHit. Align 'L, N' -> L. Unmapped: Lycanthropy infection (master writes Lycanthropy). Retaliate at +4 if young or females attacked. |
| Lycanthropes, Wereboars | Wereboar | 1d10 | 5 | 12 | 4+1 | 15 | C | 1 | 1d6 | C | B | D | SilverToHit | Align 'C, N' -> C. Unmapped: Lycanthropy infection. |
| Lycanthropes, Weretigers | Weretiger | 1d10 | 4 | 12 | 5 | 15 | C | 1 | 1d6 | C | B | D | SilverToHit | Align 'C, N' -> C. Unmapped: Lycanthropy infection. |
| Lycanthropes, Werewolves | Werewolf | 1d10 | 6 | 15 | 4 | 15 | C | 1 | 1d6 | C | B | D | SilverToHit | Align 'C, N' -> C. Unmapped: Lycanthropy infection. |
| Manticoras | Manticora | 1d4 | 5 | 12 | 6+1 | 25 | D | 1 | 1d6 | C | B | D | Flight (18), TailSpikes | DD spelling kept. Volley of 6 tail spikes within 18" -> TailSpikes (Arena: six 1d6 spike attacks), as master Manticore. |
| Mastadons | Mastodon | 1d12 | 6 | 15 | 12 | - | - | 1 | 2d6+2 | N | A | W | - | Summary spells it 'Mastadons'; the description heading is 'Mastodons'. |
| Medusae | Medusa | 1d4 | 7 | 9 | 4 | 75 | F | 1 | 1d6 | C | B | D | PetrifyingGaze, Poison | Gaze petrifies -> PetrifyingGaze; hair of deadly venomous snakes -> Poison (as master). |
| Men, Bandits | Bandit | 2d8 | 8 | 12 | 1 | 15 | A | 1 | 1d6 | C | M | D | - | Align 'C, N' -> C. Treasure A1 -> A. |
| Men, Berserkers | Berserker | 2d8 | 9 | 12 | 1+1 | 15 | A | 1 | 1d6 | N | M | W | HitBonus (2), Fearlessness | +2 to hit vs man-types -> HitBonus (2); never checks morale -> Fearlessness (as master). Unmapped: The +2 applies only against man-types. |
| Men, Brigands | Brigand | 2d8 | 6 | 12 | 1 | 15 | A | 1 | 1d6 | C | M | W | - | Unmapped: +1 morale (master writes Bravery (1)). |
| Men, Buccaneers | Buccaneer | 2d8 | 8 | 12 | 1 | 15 | A | 1 | 1d6 | C | M | W | - | Align 'C, N' -> C. Treasure A3 -> A. |
| Men, Dervishes | Dervish | 2d8 | 8 | 12 | 1+1 | 15 | A | 1 | 1d6 | L | M | W | HitBonus (2), Fearlessness | +2 to hit vs man-types and never checks morale -> HitBonus (2), Fearlessness. Treasure A2 -> A. Unmapped: The +2 applies only against man-types. |
| Men, Mercenaries | Mercenary | 2d8 | 6 | 12 | 1+1 | 15 | A | 1 | 1d6 | N | M | W | - | Treasure A3 -> A. |
| Men, Nomads | Nomad | 2d8 | 8 | 12 | 1 | 15 | A | 1 | 1d6 | C | M | W | - | Align 'C, N' -> C. Treasure A2 -> A. Unmapped: Always mounted. |
| Men, Pirates | Pirate | 2d8 | 8 | 12 | 1 | 15 | A | 1 | 1d6 | C | M | W | - | Treasure A3 -> A. Unmapped: +1 morale. |
| Men, Zealots | Zealot | 2d8 | 9 | 12 | 1+1 | 15 | A | 1 | 1d6 | C | M | W | HitBonus (2), Fearlessness | As Dervish, chaotic. Treasure A2 -> A. Unmapped: The +2 applies only against man-types. |
| Mermen | Merman | 2d6 | 7 | 3 | 1+1 | 40 | A | 1 | 1d6 | N | M | U | Swimming (15) | Treasure A3 -> A. Unmapped: +2 to hit and no morale checks vs man-types in the sea; -2 to hit and morale on land (master writes LandWeakness). Grapple ships (master writes Grappling). |
| Minotaurs | Minotaur | 1d8 | 6 | 12 | 6 | 30 | C | 1 | 1d6 | C | B | D | Fearlessness | Never checks morale -> Fearlessness (as master). Align 'C, N' -> C. Unmapped: Never gives up a chase. |
| Mummies | Mummy | 1d6 | 4 | 6 | 5+1 | 30 | D | 1 | 1d6 | C | U | D | MagicToHit (1), ChopResistance, FireVulnerability, Rotting | Invulnerable to normal weapons -> MagicToHit (1); magic weapons half damage -> ChopResistance (parameter 0 halves all weapon damage); vulnerable to fire -> FireVulnerability; necrosis slows healing tenfold -> Rotting. Identical to master Mummy. |
| Nixies | Nixie | 2d10 | 7 | 6 | 1-1 | 100 | B | 1 | 1d6 | N | F | U | Swimming (12), CharmPerTen | Any 10 nixies jointly cast charm person -> CharmPerTen (as master). Unmapped: Water breathing on the charmed victim; grappling ships with 40+. |
| Ochre jelly | Ochre Jelly | 1 | 9 | 3 | 5 | - | - | 1 | 1d6 | N | S | D | WoodEating, VoltImmunity, ChopImmunity | Dissolves wood -> WoodEating; lightning and weapons divide it harmlessly -> VoltImmunity, ChopImmunity (as master). Unmapped: Splitting into two jellies (master writes Splitting). |
| Octopi, giant | Giant Octopus | 1d4 | 7 | 0 | 4 | 30 | A | 4 | 1d6 | N | A | U | Swimming (9) | 1-6 attack rolls per turn -> Atk 4 (expected value 3.5; Arena has no random attack rate). Move '-/9' -> MV 0 plus Swimming (9). Treasure A3 -> A. Unmapped: Grapple and capsize small vessels. |
| Ogres | Ogre | 1d8 | 6 | 9 | 4+1 | 30 | C | 1 | 1d6+2 | C | H | D | - | 3-8 -> 1d6+2. Treasure C* -> C. |
| Orcs | Orc | 2d8 | 7 | 9 | 1 | 50 | D | 1 | 1d6 | C | H | D | - | Unmapped: -1 attack and morale in full daylight (master writes LightSensitivity). No morale checks defending lair at 3:1 odds. |
| Pegasi | Pegasus | 1d12 | 6 | 24 | 2+2 | - | - | 1 | 1d6 | L | F | W | Flight (48) | Align 'L, N' -> L. |
| Pixies | Pixie | 2d10 | 6 | 9 | 1-1 | 25 | C | 1 | 1d6 | N | F | W | Flight (18), Invisibility, Sleep | Permanently invisible -> Invisibility. Any 10 pixies jointly cast sleep once per day -> Sleep: a SpecialType name, but Monster.java only implements it as a condition, so documentation only (see NOTES). Unmapped: Joint sleep spell once per day (Sleep listed but inert). Always attack by surprise unless magically detected. |
| Purple worms | Purple Worm | 1d4 | 6 | 9 | 15 | 25 | D | 1 | 2d6 | N | B | D | Swallowing, Poison, Fearlessness | Swallows whole on exceeds-by-4 / 20 -> Swallowing; venomous tail stinger -> Poison; never checks morale -> Fearlessness (identical to master). Exceeds-by-4 trigger: exceeds-by-4 / natural 20: swallow whole (mapped to Swallowing). Unmapped: Secondary move 9 is burrowing. |
| Rats, giant | Giant Rat | 2d6 | 7 | 12 | 1/2 | 10 | C | 1 | 1d3 | N | A | D | Swimming (6) | 1-3 -> 1d3 (as master). Unmapped: Disease on a hit, save vs poison at +4 (master writes Disease, not an enum name). -2 morale; flee from fire. |
| Robots | Robot | 1d4 | 3 | 6 | 7 | - | - | 1 | 1d6+2 | C | B | D | Fearlessness, Disintegration | 3-8 -> 1d6+2. Never checks morale -> Fearlessness. Disintegration ray thrice per day (save vs wands) -> Disintegration: a SpecialType name, but only implemented as a condition in Monster.java, so documentation only (see NOTES). Align 'C, N' -> C. Unmapped: Disintegration ray, 6" range, 3/day (listed but inert). Many robots fly instead of having the ray. Cannot be subdued. |
| Rocs, Young | Young Roc | 1d8 | 6 | 6 | 6 | 20 | I | 1 | 1d6 | N | F | W | Flight (48) | Stats from Table 3.12; Number/Lair/Treasure/Align from the summary. Move 6/48 -> MV 6, Flight (48). Unmapped: Always spots hidden (not invisible) man-types, so master's Detection (which is about invisibility) is not used. |
| Rocs, Adult | Adult Roc | 1d6 | 5 | 6 | 12 | 20 | I | 1 | 2d6 | N | F | W | Flight (42) |  |
| Rocs, Ancient | Ancient Roc | 1d4 | 4 | 6 | 18 | 20 | I | 1 | 3d6 | N | F | W | Flight (36), Fear (2) | 'The largest rocs' force normal-types (under 3 HD) to check morale when attacked -> Fear (2) (Arena: enemies of HD 2 or less must save or flee). |
| Sabre toothed tigers | Sabre-Toothed Tiger | 1d2 | 6 | 12 | 7+2 | 15 | - | 1 | 1d8+1 | N | A | W | - | 2-9 -> 1d8+1. CRIT-DAMAGE PATTERN: 2-9 normally, 4-14 on exceeds-by-4 / natural 20. |
| Salamanders | Salamander | 1d4+1 | 5 | 9 | 7+3 | 70 | F | 1 | 2d6 | C | B | D | Constriction, FireImmunity, MagicToHit (1) | AC 3/5: upper body AC 5, serpent section AC 3; a melee opponent fights the upper body, so 5 (as master Salamander). Weapon 1-6 plus 1-6 burning to non-fire creatures -> Dam 2d6. Constricts with burning tail on exceeds-by-4 for 2-12 (+1-6) -> Constriction (Arena: attaches on any hit and does half the attack routine per round). Invulnerable to fire and normal weapons -> FireImmunity, MagicToHit (1). Number 2-5 -> 1d4+1. Exceeds-by-4 trigger: exceeds-by-4: constrict for 2-12 plus 1-6 (mapped to Constriction). Unmapped: Split AC: serpent section is AC 3 (Arena has one AC). |
| Scorpions, giant | Giant Scorpion | 1d4 | 3 | 15 | 5+4 | 50 | D | 1 | 1d6+2 | N | A | D | Poison | Pincer 3-8 -> 1d6+2. Stinger (fatal poison, save) only on exceeds-by-4 / 20 -> Poison; Arena's Poison fires on every hit, so this over-states the sting. Exceeds-by-4 trigger: exceeds-by-4 / natural 20: stinger, save vs poison or die (mapped to Poison). |
| Sea monsters, Leviathan | Leviathan | 1 | 4 | 0 | 45 | - | H | 1 | 4d6 | N | A | U | Swimming (18), Swallowing | Swallows a ship whole for 4-24 to all aboard -> Dam 4d6, Swallowing. Move '-/18' -> MV 0, Swimming (18). Unmapped: Capsizes 1-3 ships per turn. |
| Sea monsters, Kraken | Kraken | 1 | 2 | 3 | 30 | 75 | G | 4 | 3d6 | N | A | U | Swimming (18) | 1-6 attack rolls of 3-18 -> Atk 4 (expected 3.5), Dam 3d6. Treasure G* -> G. Unmapped: Capsizes any ship in 1-2 turns. Confined to a null dimension unless summoned. |
| Sea monsters, Sea serpents | Sea Serpent | 1d4 | 6 | 0 | 15 | 25 | D | 1 | 2d6 | N | A | U | Swimming (21), Swallowing | 2-12 and swallows whole 'as per purple worms' -> Dam 2d6, Swallowing. Unmapped: Encircles and destroys longboats in 1-6 turns. |
| Shadows | Shadow | 1d10 | 7 | 9 | 2+2 | 50 | F | 1 | 1d6 | C | B | D | Flight (9), SilverToHit, StrengthDrain | Move '-/9' (incorporeal) -> MV 9 plus Flight (9). Silvered or magic weapons only -> SilverToHit. Drains 1-4 strength per hit -> StrengthDrain (Arena drains 1 point per hit). Not undead in DD, so Type B as master. Unmapped: Magic weapons do double damage. Victims reduced to nil strength rise as shadows (master writes Spawn). |
| Skeletons | Skeleton | 3d10 | 8 | 6 | 1/2 | - | - | 1 | 1d6 | N | U | D | Fearlessness | Never checks morale -> Fearlessness (as master). Type U adds Undead. Unmapped: Unaffected by normal missiles. |
| Snakes, giant | Giant Viper | 1d4 | 6 | 9 | 7 | - | - | 1 | 1d6 | N | A | D | Swimming (9), Poison | DD's single 'Snakes, giant' row covers two sorts; split into Giant Viper (deadly venomous -> Poison) and Giant Constrictor Snake, like master's Giant Poisonous Snake / Giant Constrictor Snake. |
| Snakes, giant | Giant Constrictor Snake | 1d4 | 6 | 9 | 7 | - | - | 1 | 2d6 | N | A | D | Swimming (9), Constriction | Bite is only 1-2 but the real attack is crushing for 2-12 per turn -> Dam 2d6 with Constriction (Arena applies half the attack routine per round to the constricted host). Exceeds-by-4 trigger: surprise or exceeds-by-4: encircle and crush for 2-12 per turn (mapped to Constriction). Unmapped: Bite damage 1-2 when not constricting. Encircles and destroys small boats. |
| Snakes, large | Large Snake | 2d8 | 8 | 6 | 1/2 | - | - | 1 | 1d6 | N | A | D | Swimming (6), Poison | 50% are venomous -> Poison included (Arena has no 'half of them' idiom); strike it if you prefer the harmless half. |
| Spectres | Spectre | 1d8 | 3 | 15 | 6 | 25 | E | 1 | 1d6 | C | U | D | Flight (15), MagicToHit (1), EnergyDrain (2) | Move '-/15' -> MV 15, Flight (15). Impervious to normal weapons -> MagicToHit (1). Drains two levels -> EnergyDrain (2). Unmapped: Passes through walls. Slain victims rise as spectre thralls (master writes Spawn). |
| Spiders, giant | Giant Spider | 1d8 | 5 | 3 | 4+4 | 70 | C | 1 | 1d6 | C | A | D | WebMove (12), Poison, Webs | Move 3/12 -> MV 3, WebMove (12) as master. Deadly venomous -> Poison. Webs equal to a web spell -> Webs: a SpecialType name but only implemented as a condition, so documentation only (see NOTES). Align C per summary. Unmapped: Web-spell webs around the lair (Webs listed but inert). Ambush from hiding. |
| Spiders, large | Large Spider | 1d10 | 8 | 6 | 1/2 | 60 | C | 1 | 1d6 | N | A | D | Poison (2) | Venomous with save at +2 -> Poison (2) (parameter is the target's save bonus, as master Large Spider). Unmapped: Secondary move 15 is scurrying over walls and ceilings. |
| Squid, giant | Giant Squid | 1d6 | 7 | 0 | 6 | 20 | A | 4 | 1d6 | N | A | U | Swimming (12) | AC 7/3 (not explained in DD; presumably body / tentacles) -> 7, as master Giant Squid. 1-6 attack rolls -> Atk 4. Move '-/12' -> MV 0, Swimming (12). Treasure A3 -> A. Unmapped: Split AC: second value 3 (Arena has one AC). Ink cloud and triple-speed retreat (master writes InkCloud, Jet). Grapple and capsize vessels. |
| Thulls | Thull | 1d8 | 6 | 9 | 3 | 35 | D | 1 | 1d6 | C | H | D | Regeneration (1), Paralysis | Regenerates 1 hp per turn -> Regeneration (1). Scratch paralyses normal man-types -> Paralysis. Unmapped: Elves immune to the paralysis. |
| Tigers | Tiger | 1d4 | 6 | 12 | 5+4 | 15 | - | 1 | 1d6+1 | N | A | W | - | CRIT-DAMAGE PATTERN: 2-7 normally, 2-12 on exceeds-by-4 / natural 20. Unmapped: Stalks to attack by surprise. |
| Titanotheres | Titanothere | 1d12 | 7 | 12 | 12 | - | - | 1 | 3d6 | N | A | W | - |  |
| Titan | Titan | 1 | 2 | 18 | 21 | 5 | A | 1 | 3d6+3 | N | H | D | Spells | Any two magic-user or cleric spells of each level per day -> bare Spells; Monster.java gives a monster named exactly 'Titan' two spells per level (d3+3 levels). Align 'Any' -> N. Treasure A1* -> A. DD gives no magic resistance, so master's MagicResistance (60) is not carried over. |
| Toads, giant | Giant Toad | 1d6 | 6 | 6 | 2+4 | 40 | - | 1 | 1d6 | N | A | D | Swimming (6), Poison | 50% venomous -> Poison included (strike if preferred). Swallows only halflings and smaller, so Swallowing is not used against a human party. Exceeds-by-4 trigger: exceeds-by-4: swallow halfling-sized or smaller (not mapped). Unmapped: Hop 18" every other turn (master writes Leaping). |
| Treants | Treant | 1d10 | 2 | 6 | 8 | 15 | - | 1 | 2d6 | L | F | W | MagicToHit (1), ChopResistance, FireVulnerability, SummonTrees | Invulnerable to normal weapons -> MagicToHit (1); half damage from magic weapons other than axes -> ChopResistance; vulnerable to fire -> FireVulnerability; awakens trees that fight as treants -> SummonTrees (Arena summons two 'Animated Tree' rows, added below). Align 'L, N' -> L. Unmapped: Axes do full damage. |
| Treants | Animated Tree | 1 | 2 | 6 | 8 | - | - | 1 | 2d6 | L | F | W | MagicToHit (1), ChopResistance, FireVulnerability | Support row for SummonTrees (Monster.java looks up 'Animated Tree' by name). 'An awakened tree fights exactly as another treant without the ability to awaken others.' |
| Trolls | Troll | 1d6 | 5 | 12 | 6+3 | 50 | D | 1 | 1d6 | C | H | D | Regeneration (3) | Regenerates 3 hp per turn -> Regeneration (3) (as master; DD delays it three turns after injury). Tooth and claw only -> 1d6. |
| Unicorns | Unicorn | 1d4 | 3 | 24 | 4 | - | - | 1 | 1d6 | L | F | W | SaveBonus (6), Detection (24) | Saves as a 12th-level magic-user -> SaveBonus (6) (master idiom for the same text). Senses enemies within 24" -> Detection (24), as master. Unmapped: Dimension door 36" once per day (master writes DimensionDoor (36)). Horn as a lance when charging. |
| Vampires | Vampire | 1d6 | 2 | 12 | 8 | 20 | F | 1 | 1d6 | C | U | D | Flight (18), MagicToHit (1), Regeneration (3), EnergyDrain (2), Charm (-2), SummonVermin, Polymorphism | Impervious to normal weapons -> MagicToHit (1); regenerates 3/turn -> Regeneration (3); drains two levels -> EnergyDrain (2); charm gaze at -2 -> Charm (-2); calls bats/rats/wolves -> SummonVermin (Arena summons 3d6 'Wolf'); gaseous form / giant bat -> Polymorphism. Move 12/18 -> MV 12, Flight (18) (bat form). Unmapped: Forced into gaseous form at 0 hp rather than slain (master writes Undying). Slain victims rise as vampires or ghouls (master writes Spawn). Level drain only after the victim is charmed. |
| Weasels, giant | Giant Weasel | 1d8 | 6 | 15 | 2 | 15 | - | 1 | 1d6 | N | A | D | BloodDrain (4) | Holds on after exceeds-by-4 and gorges, draining 1-4 strength per turn -> BloodDrain (4) (Arena: attach and drain 1d4 per round), the closest mechanical fit even though DD drains strength rather than hp. Exceeds-by-4 trigger: exceeds-by-4: bite and hold, draining 1-4 strength per turn (mapped to BloodDrain (4)). |
| Wight apes | Wight Ape | 1d6 | 6 | 12 | 5+2 | 10 | C | 1 | 2d6-1 | N | A | D | - | 1-11 -> 2d6-1. DD's white ape. |
| Wights | Wight | 1d12 | 6 | 9 | 3 | 60 | B | 1 | 1d6 | C | U | D | SilverToHit, EnergyDrain (1) | Silvered or magic weapons only -> SilverToHit; drains one level -> EnergyDrain (1). Unmapped: Magic weapons do double damage. -2 attack and morale in daylight. Slain man-types rise as wights (master writes Spawn). |
| Wolves | Wolf | 1d10 | 7 | 18 | 1 | 15 | - | 1 | 1d6 | N | A | W | - | Named 'Wolf' so SummonVermin (vampire) can find it. |
| Wolves, giant | Giant Wolf | 1d6 | 6 | 18 | 2+2 | 15 | - | 1 | 1d6 | C | A | W | - | Unmapped: Wargs can be ridden by goblins. |
| Woolly mammoths | Woolly Mammoth | 1d12 | 5 | 15 | 13 | - | - | 1 | 3d6 | N | A | W | ColdImmunity | Invulnerable to cold -> ColdImmunity. |
| Woolly rhinoceroses | Woolly Rhinoceros | 1d4 | 5 | 12 | 10 | - | - | 1 | 2d6+2 | N | A | W | ColdImmunity | 4-14 -> 2d6+2. Invulnerable to cold -> ColdImmunity. |
| Wraiths | Wraith | 1d8 | 4 | 12 | 4 | 20 | E | 1 | 1d6 | C | U | D | Flight (12), SilverToHit, ChopResistance (1), EnergyDrain (1), Fear (2) | Move '-/12' -> MV 12, Flight (12). Silvered or magic only -> SilverToHit; silver does half damage -> ChopResistance (1) (halves damage from weapons below magic level 1, i.e. the silvered ones). Drains one level -> EnergyDrain (1). Normal man-types must check morale if attacked -> Fear (2) (Combat chapter, Morale). Unmapped: -2 attack and morale in daylight. Evil allies get +1 morale. Slain man-types rise as wraiths (master writes Spawn). |
| Wyverns | Wyvern | 1d6 | 4 | 9 | 7 | 60 | E | 1 | 1d6+2 | C | B | D | Flight (24), Poison | Bite and claw 3-8 -> 1d6+2. Stinger (deadly venom) on exceeds-by-4 / 20 -> Poison (as master; Arena's Poison fires on every hit). Align 'C, N' -> C. Exceeds-by-4 trigger: exceeds-by-4 / natural 20: tail stinger, save vs poison (mapped to Poison). |
| Yellow mold | Yellow Mold | 1 | 9 | 0 | 3 | - | - | 1 | 1d6 | N | S | D | SporeCloud, WoodEating, VoltImmunity, ColdImmunity, ChopImmunity | 50% toxic spore cloud when disturbed (save vs poison or die) -> SporeCloud; dissolves wood -> WoodEating; impervious to everything but fire -> VoltImmunity, ColdImmunity, ChopImmunity (identical to master). Move 'n/a' -> 0. |
| Zombies | Zombie | 3d10 | 9 | 6 | 1 | - | - | 1 | 1d6 | N | U | D | Fearlessness | Never checks morale -> Fearlessness (as master). Unmapped: Unaffected by normal missiles. |
