import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from lra_research import (
    ResearchError, validate_url, DocumentParser, select_sentences, run_pipeline
)


class ResearchEngineTests(unittest.TestCase):
    def test_url_allowlist_rejects_other_hosts_and_http(self):
        with self.assertRaises(ResearchError):
            validate_url("https://example.com/page", {"docs.github.com"})
        with self.assertRaises(ResearchError):
            validate_url("http://docs.github.com/page", {"docs.github.com"})
        with self.assertRaises(ResearchError):
            validate_url("https://docs.github.com.evil.test/page", {"docs.github.com"})

    def test_parser_ignores_script_content(self):
        parser = DocumentParser()
        parser.feed("<html><title>Security Guide</title><body>"
                    "<p>Use least privilege for workflow token permissions.</p>"
                    "<script>FAKE_SECRET_TEXT</script></body></html>")
        title, text = parser.result()
        self.assertEqual(title, "Security Guide")
        self.assertIn("least privilege", text)
        self.assertNotIn("FAKE_SECRET_TEXT", text)

    def test_sentence_selection_requires_keyword_match(self):
        text = ("This paragraph describes an unrelated topic in enough detail to "
                "be considered a sentence for extraction. "
                "Workflow token permissions should follow the principle of least "
                "privilege in a secure automation environment.")
        selected = select_sentences(text, ["token permissions", "least privilege"])
        self.assertEqual(len(selected), 1)
        self.assertIn("least privilege", selected[0])

    def test_pipeline_writes_evidence_and_advances_only_to_synthesis(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            mission = root / "MISSIONS" / "test-mission"
            mission.mkdir(parents=True)
            (mission / "findings").mkdir()
            (mission / "state.json").write_text(json.dumps({
                "mission_id": "test-mission", "state": "Research"
            }), encoding="utf-8")
            config = {
                "mission_id": "test-mission",
                "mission_dir": "MISSIONS/test-mission",
                "question": "How should workflow token permissions be restricted?",
                "allowed_hosts": ["docs.github.com"],
                "sources": [{
                    "url": "https://docs.github.com/en/actions/concepts/security/github_token",
                    "keywords": ["permissions", "least privilege"]
                }],
                "synthesis_groups": [{
                    "title": "Permissions", "keywords": ["permissions"]
                }]
            }
            config_path = root / "config.json"
            config_path.write_text(json.dumps(config), encoding="utf-8")
            record = {
                "url": config["sources"][0]["url"],
                "final_url": config["sources"][0]["url"],
                "status": 200,
                "title": "Token security",
                "retrieved_at": "2026-01-01T00:00:00+00:00",
                "text": "Workflow token permissions should follow the principle of least "
                        "privilege in secure automation systems. Restrict write access "
                        "to the minimum required operations."
            }
            with patch("lra_research.fetch_source", return_value=record):
                run_pipeline(config_path, root)

            state = json.loads((mission / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["state"], "Synthesize")
            research = (mission / "findings" / "research.md").read_text(encoding="utf-8")
            synthesis = (mission / "synthesis.md").read_text(encoding="utf-8")
            self.assertIn("[S1]", research)
            self.assertIn("docs.github.com", research)
            self.assertIn("[S1]", synthesis)
            self.assertFalse((mission / "artifacts" / "stage-record.md").exists())

    def test_pipeline_refuses_wrong_state(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            mission = root / "MISSIONS" / "test-mission"
            mission.mkdir(parents=True)
            (mission / "state.json").write_text(json.dumps({
                "mission_id": "test-mission", "state": "Stage"
            }), encoding="utf-8")
            config_path = root / "config.json"
            config_path.write_text(json.dumps({
                "mission_id": "test-mission",
                "mission_dir": "MISSIONS/test-mission",
                "question": "test",
                "allowed_hosts": ["docs.github.com"],
                "sources": [{"url": "https://docs.github.com/test", "keywords": ["test"]}]
            }), encoding="utf-8")
            with self.assertRaises(ResearchError):
                run_pipeline(config_path, root)


if __name__ == "__main__":
    unittest.main(verbosity=2)