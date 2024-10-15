# https://qiita.com/takayg1/items/c811bd07c21923d7ec69

from collections.abc import Callable
from typing import Generic, TypeVar

T = TypeVar("T")
K = TypeVar("K")


class SegTree(Generic[K, T]):
    """
    init(init_val, ide_ele): 配列init_valで初期化 O(N)
    update(k, x): k番目の値をxに更新 O(logN)
    query(l, r): 区間[l, r)をsegfuncしたものを返す O(logN)
    """

    def __init__(self, init_val: list[T], segfunc: Callable[[T, T], T], ide_ele,
                 compression_keys: list[K] = []):
        """
        init_val: 配列の初期値
        segfunc: 区間にしたい操作
        ide_ele: 単位元
        float_keys: 座標圧縮に使う、配列のキーとなる値

        n: 要素数
        num: n以上の最小の2のべき乗
        tree: セグメント木(1-index)
        """
        n = len(init_val)
        self.segfunc = segfunc
        self.ide_ele = ide_ele
        self.num = 1 << (n - 1).bit_length()
        self.tree = [ide_ele] * 2 * self.num

        if not compression_keys:
            compression_keys = list(range(n))
        # 座標圧縮
        if any(compression_keys[i] > compression_keys[i+1]
               for i in range(len(compression_keys) - 1)):
            compression_keys.sort()
        if any(compression_keys[i] >= compression_keys[i + 1] for i in range(n - 1)):
            compression_keys, b = [], compression_keys
            for x in b:
                if not compression_keys or compression_keys[-1] != x:
                    compression_keys.append(x)
        self._compressed_keys = {k: i for i,
                                 k in enumerate(compression_keys)}

        # 配列の値を葉にセット
        for i in range(n):
            self.tree[self.num + i] = init_val[i]
        # 構築していく
        for i in range(self.num - 1, 0, -1):
            self.tree[i] = self.segfunc(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, k: K, x: T):
        """
        k番目の値をxに更新
        k: index(0-index)
        x: update value
        """
        _k = self._compressed_keys[k]
        _k += self.num
        self.tree[_k] = x
        while _k > 1:
            self.tree[_k >> 1] = self.segfunc(self.tree[_k], self.tree[_k ^ 1])
            _k >>= 1

    def query(self, left: K, right: K):
        """
        [l, r)のsegfuncしたものを得る
        l: index(0-index)
        r: index(0-index)
        """
        res = self.ide_ele

        _left = self._compressed_keys[left]
        _right = self._compressed_keys[right]

        _left += self.num
        _right += self.num
        while _left < _right:
            if _left & 1:
                res = self.segfunc(res, self.tree[_left])
                _left += 1
            if _right & 1:
                res = self.segfunc(res, self.tree[_right - 1])
            _left >>= 1
            _right >>= 1
        return res

    def query_close(self, left: K, right: K):
        """
        [l, r](閉区間)のsegfuncしたものを得る
        l: index(0-index)
        r: index(0-index)
        """
        res = self.ide_ele

        _left = self._compressed_keys[left]
        _right = self._compressed_keys[right] + 1

        _left += self.num
        _right += self.num
        while _left < _right:
            if _left & 1:
                res = self.segfunc(res, self.tree[_left])
                _left += 1
            if _right & 1:
                res = self.segfunc(res, self.tree[_right - 1])
            _left >>= 1
            _right >>= 1
        return res

    def __getitem__(self, k: K) -> T:
        return self.tree[self.num + self._compressed_keys[k]]
