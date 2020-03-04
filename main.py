import random
import math

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


# Return the score from normal scoring only in OccurrenceValueList and the remaining OccurrenceValueDice
def analyse_turn_normal_score(dices_value_occurrence_list):
    turn_normal_score = 0

    scoring_value_index = 0
    while scoring_value_index < len(LIST_SCORING_DICE_VALUE):
        scoring_value = LIST_SCORING_DICE_VALUE[scoring_value_index]
        scoring_multiplier = LIST_SCORING_MULTIPLIER[scoring_value_index]
        turn_normal_score += dices_value_occurrence_list[scoring_value - 1] * scoring_multiplier
        dices_value_occurrence_list[scoring_value - 1] = 0

        scoring_value_index += 1

    return turn_normal_score, dices_value_occurrence_list


# Return the score from both bonus and normal scoring in OccurrenceValueList and the remaining OccurrenceValueDice
def analyse_roll_to_score(dices_value_occurrence_list):
    bonus_score, remaining_value_occurrence_list = analyse_turn_bonus_score(dices_value_occurrence_list)
    normal_score, remaining_value_occurrence_list = analyse_turn_normal_score(dices_value_occurrence_list)

    return bonus_score + normal_score, remaining_value_occurrence_list


def get_sum_remaining_dices(dices_value_occurrence_list):
    return sum(dices_value_occurrence_list)


def roll_score_distribution(nb_roll, nb_dice, interval):
    list_score = []
    list_remaining_dices = []
    list_remaining_dices_distribution = [0] * (nb_dice + 1)

    index_nb_roll = 0
    while index_nb_roll < nb_roll:
        dices = roll_dices(nb_dice)
        score, remaining_dices = analyse_roll_to_score(dices)
        sum_dices = get_sum_remaining_dices(remaining_dices)
        list_remaining_dices_distribution[sum_dices] += 1
        list_score.append(score)
        list_remaining_dices.append(remaining_dices)
        index_nb_roll += 1

    list_score_distribution = [0] * ((max(list_score) // interval) + 1)

    index_list_score = 0
    while index_list_score < len(list_score):
        list_score_distribution[math.ceil(list_score[index_list_score] / interval)] += 1
        index_list_score += 1

    index_list_score_distribution = 0
    while index_list_score_distribution < len(list_score_distribution):
        list_score_distribution[index_list_score_distribution] /= nb_roll
        index_list_score_distribution += 1

    index_list_remaining_dices_distribution = 0
    while index_list_remaining_dices_distribution < len(list_remaining_dices_distribution):
        list_remaining_dices_distribution[index_list_remaining_dices_distribution] /= nb_roll
        index_list_remaining_dices_distribution += 1

    return list_score_distribution, list_remaining_dices_distribution

def play_turn():
    is_playing = True
    dices_to_play = 5
    score = 0

    #while is_playing:
    #    dices = roll_dices(dices_to_play)
    dices = roll_dices(dices_to_play)
    print(dices)
    print(analyse_roll_to_score(dices))
    print(get_sum_remaining_dices(dices))


list_score_distribution, list_remaining_dices_distribution = (roll_score_distribution(10000, 5, 50))

print(list_score_distribution, "\n")
print(list_remaining_dices_distribution, "\n")