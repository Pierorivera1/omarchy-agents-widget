import json
import os
import runpy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


COLLECTOR = Path(__file__).resolve().parents[1] / "scripts/omarchy-agent-usage-codex"


def token_event(total, input_tokens=100, output_tokens=20):
    info = {"last_token_usage": {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cached_input_tokens": 40,
    }}
    if total is not None:
        info["total_token_usage"] = {"total_tokens": total}
    return {"type": "event_msg", "payload": {"type": "token_count", "info": info}}


class NativeUsageTests(unittest.TestCase):
    def scan(self, sessions):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "sessions"
            root.mkdir()
            for index, events in enumerate(sessions):
                context = {"type": "turn_context", "payload": {"model": "test-model"}}
                (root / f"{index}.jsonl").write_text(
                    "\n".join(json.dumps(event) for event in [context, *events]) + "\n"
                )
            with patch.dict(os.environ, {"CODEX_HOME": directory}):
                module = runpy.run_path(str(COLLECTOR), run_name="test_collector")
                module["scan_native_codex_sessions"]()
                return module["local_stats"]()

    def test_repeated_cumulative_total_is_counted_once(self):
        stats = self.scan([[token_event(120), token_event(120)]])
        self.assertEqual(stats["todayTotalTokens"], 120)
        self.assertEqual(stats["todayPrompts"], 1)
        self.assertEqual(stats["modelUsage"]["test-model"]["cacheReadInputTokens"], 40)

    def test_identical_turn_usage_with_advancing_total_is_counted(self):
        stats = self.scan([[token_event(120), token_event(240)]])
        self.assertEqual(stats["todayTotalTokens"], 240)
        self.assertEqual(stats["todayPrompts"], 2)

    def test_missing_cumulative_usage_keeps_legacy_events(self):
        stats = self.scan([[token_event(None), token_event(None)]])
        self.assertEqual(stats["todayTotalTokens"], 240)

    def test_deduplication_is_per_session(self):
        stats = self.scan([[token_event(120)], [token_event(120)]])
        self.assertEqual(stats["todayTotalTokens"], 240)
        self.assertEqual(stats["todaySessions"], 2)

    def test_cumulative_reset_is_not_discarded(self):
        stats = self.scan([[token_event(240), token_event(120)]])
        self.assertEqual(stats["todayTotalTokens"], 240)


if __name__ == "__main__":
    unittest.main()
