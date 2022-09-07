from itertools import combinations
from model_combo_flex import FlexCombo
from model_combo_qbdst import QbDstCombo
from model_player import Player
import csv


def read_player_csv():
    players = []
    with open('input_files/players.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                name = str.split(row[0], " (")[0]
                raw_id = str.split(str.split(row[0], " (")[1], ")")[0]
                name_id = row[0]
                position = row[1]
                salary = int(row[2])
                projection = float(row[3])
                ratio = float(row[4])
                player = Player(name, raw_id, position, salary)
                player.projection = projection
                player.ratio = ratio
                player.name_id = name_id
                players.append(player)
            line_count += 1
    return players


def set_position_array(position, players):
    lcl_array = []
    for element in players:
        if element.position == position:
            lcl_array.append(element)
    return sorted(lcl_array, key=lambda x: x.salary)


def set_qb_dst(qb, dst):
    temp = []
    for q in qb:
        for d in dst:
            temp.append(QbDstCombo(q, d))
    return sorted(temp, key=lambda x: x.salary)


def create_combinations(combo_list, num_of_combos):
    if num_of_combos == 2:
        temp = sorted(list(combinations(combo_list, 2)), key=lambda x: x[0].salary + x[1].salary)
    elif num_of_combos == 3:
        temp = sorted(list(combinations(combo_list, 3)), key=lambda x: x[0].salary + x[1].salary + x[2].salary)
    elif num_of_combos == 4:
        temp = sorted(list(combinations(combo_list, 4)),
                      key=lambda x: x[0].salary + x[1].salary + x[2].salary + x[3].salary)
    else:
        temp = []

    return temp


def set_max_budget(qb_dst_array):
    return 50000 - qb_dst_array[0].salary


def set_two_te_combos(max_budget, te_array, rb_array, wr_array):
    temp = []
    for te in te_array:
        for rb in rb_array:
            for wr in wr_array:
                budget = te[0].salary + te[1].salary + rb[0].salary + rb[1].salary + wr[0].salary + wr[1].salary + wr[
                    2].salary
                if budget > max_budget:
                    break
                else:
                    rb1 = rb[0]
                    rb2 = rb[1]
                    wr1 = wr[0]
                    wr2 = wr[1]
                    wr3 = wr[2]
                    te1 = te[0]
                    fx = te[1]
                    temp.append(FlexCombo(rb1, rb2, wr1, wr2, wr3, te1, fx))

    return temp


def set_three_rb_combos(max_budget, te_array, rb_array, wr_array):
    temp = []
    for te in te_array:
        for rb in rb_array:
            for wr in wr_array:
                budget = te.salary + rb[0].salary + rb[1].salary + rb[2].salary + wr[0].salary + wr[1].salary + wr[
                    2].salary
                if budget > max_budget:
                    break
                else:
                    rb1 = rb[0]
                    rb2 = rb[1]
                    wr1 = wr[0]
                    wr2 = wr[1]
                    wr3 = wr[2]
                    te1 = te
                    fx = rb[2]
                    temp.append(FlexCombo(rb1, rb2, wr1, wr2, wr3, te1, fx))

    return temp


def set_four_wr_combos(max_budget, te_array, rb_array, wr_array):
    temp = []
    for te in te_array:
        for rb in rb_array:
            for wr in wr_array:
                budget = te.salary + rb[0].salary + rb[1].salary + wr[3].salary + wr[0].salary + wr[1].salary + wr[
                    2].salary
                if budget > max_budget:
                    break
                else:
                    rb1 = rb[0]
                    rb2 = rb[1]
                    wr1 = wr[0]
                    wr2 = wr[1]
                    wr3 = wr[2]
                    te1 = te
                    fx = wr[3]
                    temp.append(FlexCombo(rb1, rb2, wr1, wr2, wr3, te1, fx))

    return temp
