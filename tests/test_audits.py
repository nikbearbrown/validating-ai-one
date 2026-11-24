"""Run reader entry points against published and contradictory cases."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIXED = json.loads((ROOT / "fixtures/audits.json").read_text())


def run(*paths):
    return subprocess.run(
        [sys.executable, "-B", str(ROOT / "lab/check_audits.py"), *map(str, paths)],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )


class CompactAudits(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p = run()
        if p.returncode:
            raise RuntimeError(p.stderr)
        cls.fixed = json.loads(p.stdout)

    def changed(self, edit, valid=True):
        d = copy.deepcopy(FIXED)
        edit(d)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "countercase.json"
            path.write_text(json.dumps(d))
            p = run(path)
        self.assertEqual(p.returncode, 0 if valid else 2, p.stderr)
        if valid:
            return json.loads(p.stdout)
        self.assertEqual(p.stdout, "")
        self.assertIn("Fixture rejected:", p.stderr)

    def test_same_decisions_different_probability_quality(self):
        models = self.fixed["forecasts"]["models"]
        self.assertEqual(models["a"], {"correct": 28, "brier": "1/5"})
        self.assertEqual(models["b"], {"correct": 28, "brier": "97/400"})
        self.assertEqual(self.fixed["reserve_above"], "1/5")

    def test_counts_reject_events_above_total(self):
        self.changed(lambda d: d["forecasts"][0].update(observed=11), valid=False)

    def test_probability_rejects_value_outside_bounded_scale(self):
        self.changed(lambda d: d["forecasts"][0].update(a="1.01"), valid=False)

    def test_equal_level_aggregate_keeps_lost_and_gained_pairs(self):
        pairs = self.fixed["pairs"]
        self.assertEqual((pairs["base_correct"], pairs["variant_correct"]), (3, 3))
        self.assertEqual(pairs["lost"], ["Harbor after"])
        self.assertEqual(pairs["gained"], ["Oak before"])

    def test_coverage_and_success_not_collapsed(self):
        pairs = self.changed(lambda d: d["pairs"][0].update(variant=None))["pairs"]
        self.assertEqual(pairs["variant_timeouts"], ["Oak after"])
        self.assertEqual((pairs["attempted"], pairs["variant_returned"], pairs["variant_correct"]), (4, 3, 2))

    def test_distinct_group_results_despite_equal_false_alarm_rate(self):
        burden = self.fixed["burdens"]
        self.assertEqual(burden["pooled_miss_rate"], "12/35")
        web, desk = [burden["channels"][k] for k in ("Web", "Desk")]
        self.assertEqual(web["fp_rate"], desk["fp_rate"])
        self.assertEqual((web["fn_rate"], desk["fn_rate"]), ("1/5", "2/5"))
        self.assertEqual((web["precision"], desk["precision"]), ("2/3", "6/7"))

    def test_empty_rate_denominator_is_unknown_not_zero(self):
        burden = self.changed(lambda d: d["channels"]["Desk"].update(tp=0, fn=0))["burdens"]
        self.assertIsNone(burden["channels"]["Desk"]["fn_rate"])

    def test_workflow_dispositions_exact(self):
        self.assertEqual(self.fixed["workflows"], {
            "clean_plan": "proposal_for_human_review_only",
            "wrong_effect": "stop_out_of_scope_effect_or_trace",
            "stale_evidence": "stop_stale_evidence",
            "lost_receipt": "stop_expected_receipt_missing",
        })

    def test_final_state_cannot_erase_prohibited_operation(self):
        result = self.changed(
            lambda d: d["workflows"]["clean_plan"]["trace"].extend([["set_hold", "R12"], ["unset_hold", "R12"]])
        )["workflows"]["clean_plan"]
        self.assertEqual(result, "stop_out_of_scope_effect_or_trace")

    def test_unchanged_trace_cannot_erase_an_observed_effect(self):
        result = self.changed(
            lambda d: d["workflows"]["clean_plan"].update(status="held")
        )["workflows"]["clean_plan"]
        self.assertEqual(result, "stop_out_of_scope_effect_or_trace")

    def test_capstone_uses_the_operation_it_actually_proposes(self):
        result = self.changed(
            lambda d: d["capstone"]["workflow"]["trace"][1].__setitem__(0, "propose_hold")
        )["capstone_checks"]["workflow"]
        self.assertEqual(result, "stop_out_of_scope_effect_or_trace")

    def test_malformed_trace_step_cannot_pass(self):
        self.changed(
            lambda d: d["workflows"]["clean_plan"]["trace"][1].append("not_supported"),
            valid=False,
        )

    def test_capstone_checks_the_right_axis(self):
        cap = self.fixed["capstone_checks"]
        self.assertEqual(cap["misses"], ["1/4", "1/2"])
        self.assertEqual(cap["cohorts"], ["1/5", "2/5", "3/5"])
        self.assertEqual(cap["pooled_event_rate"], "2/5")
        self.assertEqual(cap["extractions"]["variant_timeouts"], ["M3"])
        self.assertEqual(cap["extractions"]["variant_correct"], 3)
        self.assertEqual(cap["workflow"], "stop_stale_evidence")
