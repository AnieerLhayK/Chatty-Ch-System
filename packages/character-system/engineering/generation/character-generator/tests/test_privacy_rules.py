import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from anonymize_corpus import anonymize_text


class PrivacyRulesTest(unittest.TestCase):
    def test_phone_and_email_are_redacted(self):
        text = "请联系 13812345678 或 test@example.com，微信 wx_abcdef。"
        sanitized, counts = anonymize_text(text, "high")
        self.assertNotIn("13812345678", sanitized)
        self.assertNotIn("test@example.com", sanitized)
        self.assertIn("[PHONE_REDACTED]", sanitized)
        self.assertIn("[EMAIL_REDACTED]", sanitized)
        self.assertGreaterEqual(counts["phones"], 1)
        self.assertGreaterEqual(counts["emails"], 1)


if __name__ == "__main__":
    unittest.main()
