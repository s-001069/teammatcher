import numpy as np


def team_homogeneity_score(team_matrix, homogeneous_idx):
    X = team_matrix[:, homogeneous_idx]
    if len(X) <= 1:
        return 0.0
    Xn = X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-8)
    sim = Xn @ Xn.T
    n = len(X)
    return sim[np.triu_indices(n, 1)].mean()

def team_diversity_score(team_matrix, heterogeneous_idx):
    X = team_matrix[:, heterogeneous_idx]
    if len(X) <= 1:
        return 0.0
    dists = np.linalg.norm(X[:, None, :] - X[None, :, :], axis=2)
    n = len(X)
    return dists[np.triu_indices(n, 1)].mean()

def team_size_penalty(team_indices, target_size):
    return abs(len(team_indices) - target_size)

def make_fitness_func(students_encoded, team_size, weights, homogeneous_idx, heterogeneous_idx):
    """
    weights: (w_avail, w_commit, w_age, w_sex, w_job, w_bach)
    """
    w_avail, w_commit, w_age, w_sex, w_job, w_bach = weights

    def fitness_func(ga_instance, solution, solution_idx):
        solution_int = np.asarray(solution, dtype=int)
        num_teams = solution_int.max() + 1

        total_hom = 0.0
        total_div = 0.0
        size_pen = 0.0
        valid_teams = 0

        for t in range(num_teams):
            idx = np.where(solution_int == t)[0]
            if len(idx) == 0:
                continue

            team_matrix = students_encoded[idx]
            total_hom += _team_homogeneity_score(team_matrix, homogeneous_idx)
            total_div += _team_diversity_score(team_matrix, heterogeneous_idx)
            size_pen  += _team_size_penalty(idx, team_size)
            valid_teams += 1

        if valid_teams == 0:
            return 0.0

        avg_hom = total_hom / valid_teams
        avg_div = total_div / valid_teams

        fitness = (
            w_avail * avg_hom +
            w_commit * avg_hom +
            w_age * avg_div +
            w_sex * avg_div +
            w_job * avg_div +
            w_bach * avg_div
            - 2.0 * size_pen
        )

        return float(fitness)

    return fitness_func
