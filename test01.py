import random
import string
import itertools
import os

OUTPUT_DIR = "testcases"


def generate_one_testcase_cell_labeled(N=5, P=5, low=-5, high=10, seed=None,
                                       max_attempts=1000, global_attempts=100):
    random.seed(seed)
    values = list(range(low, high + 1))

    # 열별 타겟 합 생성
    for _ in range(global_attempts):
        col_targets = []
        for _ in range(P):
            pool = list(range(2*low, 2*high + 1))
            chosen = random.sample(pool, N)
            chosen.sort(reverse=True)
            col_targets.append(chosen)

        mat1 = [[0]*P for _ in range(N)]
        mat2 = [[0]*P for _ in range(N)]

        try:
            # 각 열 채우기
            for j in range(P):
                targets = col_targets[j]
                # 랜덤 시도
                for _ in range(max_attempts):
                    col_b = random.sample(values, N)
                    col_a = [targets[i] - col_b[i] for i in range(N)]
                    if all(low <= a <= high for a in col_a) and len(set(col_a)) == N:
                        for i in range(N):
                            mat1[i][j] = col_a[i]
                            mat2[i][j] = col_b[i]
                        break
                else:
                    raise ValueError
            break
        except ValueError:
            continue
    else:
        raise RuntimeError("Failed to generate valid testcase")

    # 셀 레이블 (열 우선 A..Y)
    labels = list(string.ascii_uppercase[:N*P])
    name_mat = [[None]*P for _ in range(N)]
    idx = 0
    for col in range(P):
        for row in range(N):
            name_mat[row][col] = labels[idx]
            idx += 1

    return name_mat, mat1, mat2


def solve_case(name_mat, mat1, mat2):
    players = []
    for i in range(5):
        for j in range(5):
            label = name_mat[i][j]
            cost  = 5 - i
            aval  = mat1[i][j]
            bval  = mat2[i][j]
            players.append((label, cost, j, aval, bval))

    best_score = -1
    best_sel   = None
    for r in range(5, 8):
        for combo in itertools.combinations(players, r):
            roles = set()
            cost_sum = sum(p[1] for p in combo)
            sumA = sum(p[3] for p in combo)
            sumB = sum(p[4] for p in combo)
            roles = {p[2] for p in combo}
            if cost_sum <= 18 and len(roles) == 5:
                score = sumA * sumB
                if score > best_score:
                    best_score = score
                    best_sel   = combo

    names = sorted(p[0] for p in best_sel)
    return best_score, names


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # 20개 파일 생성
    for idx in range(1, 21):
        name_mat, m1, m2 = generate_one_testcase_cell_labeled(seed=idx)
        infile = os.path.join(OUTPUT_DIR, f"{idx}.in")
        outfile = os.path.join(OUTPUT_DIR, f"{idx}.out")

        # 입력 파일 작성
        with open(infile, 'w') as f:
            for row in m1:
                f.write(" ".join(f"{v}" for v in row) + "\n")
            f.write("\n")
            for row in m2:
                f.write(" ".join(f"{v}" for v in row) + "\n")

        # 정답 계산 후 출력 파일 작성
        score, names = solve_case(name_mat, m1, m2)
        with open(outfile, 'w') as f:
            f.write(f"{score}\n")
            f.write(" ".join(names) + "\n")

    print(f"20 test case files created in ./{OUTPUT_DIR}/")
