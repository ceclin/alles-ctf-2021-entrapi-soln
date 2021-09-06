import pickle
from pathlib import Path

js_size = 1660
js = [-1 for _ in range(js_size)]


def same(i: int, j: int):
    assert i != j
    if i < j:
        if js[i] == -1:
            js[i] = i
        js[j] = js[i]
        print(f"js[{i}] == js[{j}]")
    else:
        same(j, i)


cache = Path("main.js.pickle")
table = pickle.loads(cache.read_bytes()) if cache.exists() else {}


def get(i: int, j: int) -> int:
    assert (i, j) in table
    return table[i, j]


def check(i: int):
    if get(i, i + 2) == 1:
        same(i, i + 1)
        return
    for j in range(i + 2, js_size):
        x = get(i, j)
        if x == get(i, j + 1) and x != get(i + 1, j) and x == get(i + 1, j + 1):
            same(i, j)
            break


if __name__ == "__main__":
    for i in range(js_size - 1):
        check(i)
    Path("js.pickle").write_bytes(pickle.dumps(js))
