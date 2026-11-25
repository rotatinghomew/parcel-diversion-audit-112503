"""从项目根目录执行资料契约检查。"""
from pathlib import Path
import json
import unittest

import numpy as np
from scipy import sparse

DATA = Path(__file__).resolve().parents[1] / "资料"

def load(name):
    """读取已经登记的 UTF-8 JSON 资料。"""
    with (DATA / f"{name}.json").open(encoding="utf-8") as source:
        return json.load(source)

KEYS = {'入口件': 'parcel', '读码原始记录': 'id', '分区交接': 'event', '签收回单': 'proof'}
REFERENCES = [('读码原始记录', 'direct', '入口件', 'parcel'), ('分区交接', 'parcel', '入口件', 'parcel'), ('签收回单', 'parcel', '入口件', 'parcel')]

class MaterialChecks(unittest.TestCase):
    def test_identity(self):
        """检查来源主键与登记范围。"""
        for collection, field in KEYS.items():
            with self.subTest(collection=collection):
                entries = load(collection)
                self.assertTrue(entries)
                values = [r[field] for r in entries]
                self.assertEqual(len(set(values)), len(entries))
                self.assertNotIn(None, values)

    def test_references(self):
        """核对资料表之间的引用，不改变原记录。"""
        for origin, source_field, target, target_field in REFERENCES:
            with self.subTest(origin=origin, field=source_field):
                codes = {r[target_field] for r in load(target)}
                for row in load(origin):
                    if row[source_field] is not None:
                        self.assertIn(row[source_field], codes)

    def test_data_runtime(self):
        """确认锁定的数组和稀疏矩阵依赖可用，并读取本项目资料。"""
        sizes = np.array([len(load(name)) for name in KEYS], dtype=np.int64)
        self.assertTrue(np.all(sizes > 0))
        self.assertEqual(int(sparse.csr_matrix(sizes.reshape(1, -1)).sum()), int(sizes.sum()))

    def test_related_material(self):
        """检查业务记录、变动与交接凭据是否实际存在。"""
        parcels = {r["parcel"]: r for r in load("入口件")}
        scans = {r["id"]: r for r in load("读码原始记录")}
        self.assertTrue(all(k in parcels for r in scans.values() for k in r["alternatives"]))
        routing = load("班次路由")
        self.assertTrue(all(r["parcel"] in parcels for r in routing["in_transit"]))
        for repeat in routing["additional_reads"]:
            self.assertIn(repeat["parcel"], scans[repeat["read"]]["alternatives"])
            self.assertGreater(repeat["known_at"], scans[repeat["read"]]["minute"])
