/******************************************************************************
*  Special ability types.
*  
*  Adding new types:
*  - Only add here if you also implement in code.
*  - All names here should be nouns or noun phrases.
*  - Add to category case methods as appropriate.
*
*  @author   Daniel R. Collins (dcollins@superdan.net)
*  @since    2017-07-24
******************************************************************************/

public enum SpecialType {

	//--------------------------------------------------------------------------
	//  Enumeration
	//--------------------------------------------------------------------------

	NPC, Poison, Paralysis, Petrification, BloodDrain, EnergyDrain,
	Constriction, Corrosion, Immolation, Rotting, Swallowing,
	SilverToHit, MagicToHit, ChopImmunity, DamageReduction,
	Multiheads, Berserking, HitBonus, Invisibility, Detection, 
	Grabbing, SporeCloud, RockHurling, TailSpikes, Charm, Fear,
	SaveBonus, DodgeGiants, Regeneration, StrengthDrain, Absorption,
	Whirlwind, WallOfFire, ConeOfCold, AcidSpitting, Confusion, 
	Displacement, Blinking, Phasing, CharmTouch, Dragon, 
	FireBreath, ColdBreath, VoltBreath, AcidBreath, PoisonBreath, 
	PetrifyingBreath, PetrifyingGaze, SummonVermin, SummonTrees,
	MindBlast, BrainConsumption, SappingStrands, Slowing, 
	FireImmunity, ColdImmunity, AcidImmunity, VoltImmunity, 
	SteamBreath, Stench, ResistStench, Webs, WebMove, Sleep, 
	Hold, Blindness, Polymorphism, Undead, Golem, Death, Spells,
	ManyEyeFunctions, MagicResistance, MagicImmunity, UndeadImmunity,
	Fearlessness, ProtectionFromEvil;
	
	//--------------------------------------------------------------------------
	//  Methods
	//--------------------------------------------------------------------------

	/**
	*  Find special type matching a string.
	*/
	static public SpecialType findByName (String s) {
		for (SpecialType t: SpecialType.values()) {
			if (s.equals(t.name())) {
				return t;
			}
		}
		return null;
	}
	
	/**
	*	Map condition to appropriate saving throw type.
	*/
	public SavingThrows.Type getSaveType () {
		switch (this) {

			// Spells saves
			case Charm: case Sleep: case Confusion:
			case Blindness: case Fear: case Polymorphism:
				return SavingThrows.Type.Spells; 

			// Stone saves
			case Paralysis: case Petrification: 
			case Hold: case Webs:
				return SavingThrows.Type.Stone;

			// Death saves
			case Poison: case SporeCloud: case Death:
				return SavingThrows.Type.Death; 
		}	
		System.err.println("Error: No saveType for condition: " + this);
		return null;
	}	
	
	/**
	*  Does this confer a disabling condition?
	*/
	public boolean isDisabling () {
		switch (this) {
			case Poison: case Paralysis: case Petrification: 
			case Swallowing: case SporeCloud: case Absorption: 
			case Fear: case MindBlast: case Sleep: case Charm:
			case Hold: case Webs: case Polymorphism: case Death:
				return true;
		}
		return false;
	}

	/**
	*  Is this a breath weapon?
	*/
	public boolean isBreathWeapon () {
		switch (this) {
			case FireBreath: case ColdBreath: case AcidBreath:
			case VoltBreath: case PoisonBreath: case SteamBreath:
			case PetrifyingBreath:
				return true;
		}	
		return false;
	}
	
	/**
	*  Is this a gaze weapon?
	*/
	public boolean isGazeWeapon () {
		switch (this) {
			case PetrifyingGaze: case Confusion: 
				return true;
		}	
		return false;
	}
	
	/**
	*  Is this a summons ability?
	*/
	public boolean isSummonsAbility () {
		switch (this) {
			case SummonVermin: case SummonTrees:
				return true;
		}	
		return false;
	}

	/**
	*  Is this a mental attack form?
	*/
	public boolean isMentalAttack () {
		switch (this) {
			case Charm: case Hold: case Sleep:
			case Fear: case Confusion: case MindBlast:
				return true;
		}	
		return false;
	}
	
	/**
	*  Is the undead class immune to this?
	*
	*  OD&D is explicit that charm, hold, and sleep don't affect undead.
	*  For simplicity & utility, we assume that includes any mental attack.
	*  (1E also expands that to poison, paralysis, cold, and death spell.)
	*/
	public boolean isUndeadImmune () {
		return isMentalAttack();
	}
}
