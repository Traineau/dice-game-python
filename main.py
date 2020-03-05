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
    list_remaining_dices_distribution = [0] * (nb_dice + 1)

    index_nb_roll = 0
    while index_nb_roll < nb_roll:
        score, remaining_dices = analyse_roll_to_score(roll_dices(nb_dice))

        list_remaining_dices_distribution[nb_dice - sum(remaining_dices)] += 1
        list_score.append(score)

        index_nb_roll += 1

    max_score = max(list_score)
    list_score_distribution = [0] * ((max_score // interval) + 1)

    index_list_score = 0
    while index_list_score < len(list_score):
        score_occurrence_index = math.ceil(list_score[index_list_score] / interval)
        list_score_distribution[score_occurrence_index] += 1
        index_list_score += 1

    list_score_distribution = [n / nb_roll for n in list_score_distribution]
    list_remaining_dices_distribution = [n / nb_roll for n in list_remaining_dices_distribution]

    return max_score, list_score_distribution, list_remaining_dices_distribution


def play_until_fail(nb_dice):
    nb_dice_to_launch = nb_dice
    can_launch_dices = True
    total_score = 0
    while can_launch_dices:
        score, remaining_dices = analyse_roll_to_score(roll_dices(nb_dice_to_launch))
        if score == 0:
            can_launch_dices = False
        else:
            total_score += score
            nb_dice_to_launch = sum(remaining_dices) if sum(remaining_dices) != 0 else nb_dice

    return total_score


def turn_score_distribution(nb_turn, nb_dice, interval):
    score_list = []

    roll_index = 0
    while roll_index < nb_turn:
        score_list.append(play_until_fail(nb_dice))
        roll_index += 1

    max_roll_score = max(score_list)

    score_occurrence_list = [0] * ((max_roll_score // interval) + 2)

    roll_index = 0
    while roll_index < nb_turn:
        score_occurrence_index = math.ceil(score_list[roll_index] / interval)
        score_occurrence_list[score_occurrence_index] += 1
        roll_index += 1

    occurrence_index = 0
    while occurrence_index < len(score_occurrence_list):
        score_occurrence_list[occurrence_index] /= nb_turn
        occurrence_index += 1

    return max_roll_score, score_occurrence_list


max_score, score_occurrence_list = (turn_score_distribution(10000, 5, 200))

print(max_score, "\n")
print(score_occurrence_list, "\n")

print(play_until_fail(5))
