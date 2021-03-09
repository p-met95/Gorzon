# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 08:58:20 2021

@author: rcf004
"""
import pokepy as pp
import pandas as pd
from pytablewriter import UnicodeTableWriter
import enchant

tc = pd.read_csv('bot/dictionaries/typechart.csv', index_col=0)


def weak_table(t1, t2=None):
    if t2 is None:
        w_type = tc.loc[tc[t1] > 1].index
        weak = UnicodeTableWriter()
        t_name = f"{t1} Type Weaknesses"
        weak.headers = ["Type", "Effectiveness"]
        weak.value_matrix = [[t, f'\t\t {tc[t1][t]}x'] for t in w_type]

    else:
        w_type = tc.loc[tc[t1] * tc[t2] > 1].index
        weak = UnicodeTableWriter()
        t_name = f"{t1}/{t2} Type Weaknesses"
        weak.headers = ["Type", "Effectiveness"]
        weak.value_matrix = [[t, f'\t\t {(tc[t1] * tc[t2])[t]}x'] for t in w_type]

    return t_name, weak


def res_table(t1, t2=None):
    if t2 is None:
        r_type = tc.loc[tc[t1] < 1].index

        res = UnicodeTableWriter()
        t_name = f"{t1} Type Resistances"
        res.headers = ["Type", "Effectiveness"]
        res.value_matrix = [[t, f'\t\t {tc[t1][t]}x'] for t in r_type]

    else:
        r_type = tc.loc[tc[t1] * tc[t2] < 1].index

        res = UnicodeTableWriter()
        t_name = f"{t1}/{t2} Type Resistances"
        res.headers = ["Type", "Effectiveness"]
        res.value_matrix = [[t, f'\t\t {(tc[t1] * tc[t2])[t]}x'] for t in r_type]

    return t_name, res


def suggester(word, dct):
    dictio = enchant.request_pwl_dict(f"bot/dictionaries/{dct}.txt")
    if dictio.check(word):
        return True
    else:
        return dictio.suggest(word)


def g_types(poke, cli):
    pokemon = cli.get_pokemon(poke)
    t1 = pokemon.types[0].type.name.title()
    t2 = None
    try:
        t2 = pokemon.types[1].type.name.title()
    except IndexError:
        pass

    return t1, t2


def g_ability(ability, cli):
    ab = cli.get_ability(ability)
    return ab.effect_entries[1].short_effect


def g_move(move, cli):
    mv = cli.get_move(move)
    pwr = mv.power
    acc = mv.accuracy
    typ = mv.type.name
    eff = mv.effect_entries[0].short_effect
    if '$effect_chance' in eff:
        eff_c = mv.effect_chance
        eff.replace('$effect_chance', str(eff_c))
    format_out = f'Power: **{pwr}**, Accuracy: **{acc}**, Type: **{typ.title()}**.\n{eff}'
    return format_out

