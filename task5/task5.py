import numpy as np
import json


def is_str(str_var) -> bool:
    return isinstance(str_var, str)


def get_ranking_len(ranking: list) -> int:
    ranking_len = 0
    for ranking_group in ranking:
        if is_str(ranking_group):
            ranking_len += 1
        else:
            ranking_len += len(ranking_group)
    return ranking_len


def get_relation_matrix(ranking: list) -> list:
    ranks_amount = get_ranking_len(ranking)
    relation_matrix = np.array([[0 for _ in range(ranks_amount)] for _ in range(ranks_amount)])
    for rank_group_ind, rank_group in enumerate(ranking):
        rank_list = [0 for _ in range(ranks_amount)]
        for remaining_group in ranking[rank_group_ind:]:
            if is_str(remaining_group):
                rank_list[int(remaining_group) - 1] = 1
            else:
                for remaining_rank in remaining_group:
                    rank_list[int(remaining_rank) - 1] = 1
        if is_str(rank_group):
            relation_matrix[:][int(rank_group) - 1] = rank_list
        else:
            for rank in rank_group:
                relation_matrix[:][int(rank) - 1] = rank_list
    return relation_matrix


def task(ranking_l: str, ranking_r: str) -> list:
    ranking_l = json.loads(ranking_l)
    ranking_r = json.loads(ranking_r)
    relation_matrix_l = get_relation_matrix(ranking_l)
    relation_matrix_r = get_relation_matrix(ranking_r)

    y = relation_matrix_l * relation_matrix_r
    y_transposed = relation_matrix_l.T * relation_matrix_r.T
    core = y | y_transposed
    conflicts = np.where(core == 0)
    conflict_pairs = [[str(conflict[0] + 1), str(conflict[1] + 1)] for conflict in conflicts if conflict[0] < conflict[1]]
    return json.dumps(conflict_pairs)
