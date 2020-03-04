import random

# ----------------------< Game rules constants  >-----------------------------------------------------------------------

# Number of dices by default in the set
DEFAULT_DICES_NB = 5
# Target total score to win by default
DEFAULT_TARGET_SCORE = 2000
# Number of side of the dices used in the game
NB_DICE_SIDE = 6

# List of dice value scoring
LIST_SCORING_DICE_VALUE = [1, 5]
# List of associated score for scoring dice values
LIST_SCORING_MULTIPLIER = [100, 50]

# Trigger for multiple bonus
TRIGGER_OCCURRENCE_FOR_BONUS = 3
# Special bonus multiplier for multiple ace bonus
BONUS_VALUE_FOR_ACE_BONUS = 1000
# Standard multiplier for multiple dices value bonus
BONUS_VALUE_FOR_NORMAL_BONUS = 100


def roll_dices(nb_dice_to_roll):
    dices_value_occurrence_list = [0] * NB_DICE_SIDE
    dice_index = 0
    while dice_index < nb_dice_to_roll:
        dice_value = random.randint(1, NB_DICE_SIDE)
        dices_value_occurrence_list[dice_value - 1] += 1
        dice_index += 1

    return dices_value_occurrence_list


# Return the score from bonus only in OccurrenceValueList and the remaining OccurrenceValueDice
def analyse_turn_bonus_score(dices_value_occurrence_list):
    turn_bonus_score = 0

    dices_index = 0
    while dices_index < NB_DICE_SIDE:
        dice_value = dices_index + 1
        bonus_occurrence = dices_value_occurrence_list[dices_index] // TRIGGER_OCCURRENCE_FOR_BONUS
        if bonus_occurrence >= 1:
            if dice_value == 1:
                bonus_multiplier = BONUS_VALUE_FOR_ACE_BONUS
            else:
                bonus_multiplier = BONUS_VALUE_FOR_NORMAL_BONUS

            turn_bonus_score += bonus_occurrence * bonus_multiplier * dice_value

            dices_value_occurrence_list[dices_index] %= TRIGGER_OCCURRENCE_FOR_BONUS

        dices_index += 1

    return turn_bonus_score, dices_value_occurrence_list


def analyse_turn_normal_score(dices_value_occurrence_list):
    turn_normal_score = 0

    index = 0
    while index < len(LIST_SCORING_DICE_VALUE):
        scoring_dice_index = LIST_SCORING_DICE_VALUE[index] - 1
        turn_normal_score += dices_value_occurrence_list[scoring_dice_index] * LIST_SCORING_MULTIPLIER[index]
        dices_value_occurrence_list[scoring_dice_index] = 0

        index += 1

    return turn_normal_score, dices_value_occurrence_list


def analyse_roll_to_score(dices_value_occurrence_list):
    bonus_score, dices_value_occurrence_list = analyse_turn_bonus_score(dices_value_occurrence_list)
    normal_score, dices_value_occurrence_list = analyse_turn_normal_score(dices_value_occurrence_list)

    return bonus_score + normal_score, dices_value_occurrence_list


dices = roll_dices(10)
print(dices)
print(analyse_roll_to_score(dices))
