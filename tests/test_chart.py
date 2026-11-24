"""Exercise the same CLI students see and check the actual published figure."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
NS = {"s": "http://www.w3.org/2000/svg"}


def run(path, *args):
    return subprocess.run(
        [sys.executable, "-B", str(ROOT / "lab/check_chart.py"), str(path), *args],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )


class ChartEvidence(unittest.TestCase):
    def fixture(self, s):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "case.csv"
            path.write_text(s, encoding="utf-8")
            return run(path)

    def test_main_fixture_count_tie_only(self):
        p = run("fixtures/visits.csv")
        self.assertEqual(p.returncode, 0, p.stderr)
        result = json.loads(p.stdout)
        self.assertTrue(result["tie_on_change_visits"])
        self.assertFalse(result["tie_on_baseline_fraction"])
        self.assertEqual(result["sites"]["Oak"]["baseline_fraction"], "1/4")
        self.assertEqual(result["sites"]["Harbor"]["baseline_fraction"], "1/8")

    def test_transfer_ratio_tie_only(self):
        p = run("fixtures/transfer.csv")
        self.assertEqual(p.returncode, 0, p.stderr)
        result = json.loads(p.stdout)
        self.assertEqual(
            [(i["change_visits"], i["baseline_fraction"]) for i in result["sites"].values()],
            [(5, "1/8"), (10, "1/8")],
        )
        self.assertFalse(result["tie_on_change_visits"])
        self.assertTrue(result["tie_on_baseline_fraction"])

    def test_zeros_are_not_equal_percentage_gains(self):
        p = self.fixture("site,before,after\nOak,0,9\nHarbor,0,9\n")
        result = json.loads(p.stdout)
        self.assertTrue(result["tie_on_change_visits"])
        self.assertIsNone(result["sites"]["Oak"]["baseline_fraction"])
        self.assertIsNone(result["tie_on_baseline_fraction"])

    def test_falling_counts_preserve_negative_sign(self):
        p = self.fixture("site,before,after\nOak,30,18\nHarbor,80,72\n")
        result = json.loads(p.stdout)
        self.assertEqual(result["sites"]["Oak"]["baseline_fraction"], "-2/5")
        self.assertEqual(result["sites"]["Harbor"]["change_visits"], -8)

    def test_bad_fixtures_fail_without_partial_success(self):
        for body in (
            "name,before,after\nOak,12,10\nHarbor,5,3\n",
            "site,before,after\nOak,12,10\nOak,5,3\n",
            "site,before,after\nOak,12,10\nHarbor,3\n",
            "site,before,after\nOak,12,10\nHarbor,5,3,7\n",
            "site,before,after\nOak,12,10\nHarbor,-5,3\n",
            "site,before,after\nOak,12,10\nHarbor,5,3.5\n",
            "site,before,after\nOak,12,10\n",
        ):
            with self.subTest(body=body):
                p = self.fixture(body)
                self.assertEqual(p.returncode, 2)
                self.assertEqual(p.stdout, "")
                self.assertIn("Fixture rejected:", p.stderr)

    def test_svg_tracks_source_and_actual_geometry(self):
        p = run("fixtures/visits.csv", "--svg")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(p.stdout, (ROOT / "figures/library-visits.svg").read_text())
        svg = ET.fromstring(p.stdout)
        cases = {"Oak-Before": 40, "Oak-After": 50, "Harbor-Before": 80, "Harbor-After": 90}
        for name, count in cases.items():
            with self.subTest(name=name):
                bar = svg.find(f".//s:rect[@id='{name}']", NS)
                label = svg.find(f".//s:text[@id='{name}-value']", NS)
                self.assertEqual(int(bar.get("height")), 2 * count)
                self.assertEqual(int(bar.get("y")) + 2 * count, 352)
                self.assertEqual(label.text, str(count))
        description = svg.find("s:desc", NS).text
        self.assertIn("Oak: 40 before, 50 after.", description)
        self.assertIn("Harbor: 80 before, 90 after.", description)

    def test_check_is_not_an_inference_engine(self):
        data = json.loads(run("fixtures/visits.csv").stdout)
        self.assertNotIn("recommendation", data)
        self.assertNotIn("cause", data)
        self.assertEqual(run("fixtures/transfer.csv", "--svg").returncode, 2)


if __name__ == "__main__":
    unittest.main()
