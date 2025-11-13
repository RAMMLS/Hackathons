import re
import unicodedata
import json
import logging

logger = logging.getLogger(__name__)


class UnifiedValidator:
    def __init__(self, compiled_patterns, llm):
        self.compiled_patterns = compiled_patterns
        self.llm = llm

    # === Preprocess ===
    @staticmethod
    def strip_html_tags(text: str) -> str:
        return re.sub(r"<.*?>", "", text)

    @staticmethod
    def remove_invisible_chars(text: str) -> str:
        return "".join(ch for ch in text if unicodedata.category(ch)[0] != "C")

    @staticmethod
    def normalize_unicode(text: str) -> str:
        return unicodedata.normalize("NFKC", text)

    @staticmethod
    def clean_spaces(text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()

    def preprocess_text(self, text: str) -> str:
        text = self.strip_html_tags(text)
        text = self.remove_invisible_chars(text)
        text = self.normalize_unicode(text)
        text = self.clean_spaces(text)
        return text

    # === Regex ===
    def detect_injection(self, text: str) -> bool:
        return any(pattern.search(text) for pattern in self.compiled_patterns)

    def get_detected_patterns(self, text: str) -> list[str]:
        return [p.pattern for p in self.compiled_patterns if p.search(text)]

    # === LLM intent ===
    def ask_intent_llm(self, cleaned_text: str, matched_patterns: list[str]):
        user_text = "User_input: <<USER_INPUT>>\nMatched_patterns: <<MATCHED_PATTERNS>>" \
            .replace("<<USER_INPUT>>", cleaned_text) \
            .replace("<<MATCHED_PATTERNS>>", json.dumps(matched_patterns))

        messages = [
            {"role": "system", "text": self.llm.system_prompt},
            {"role": "user", "text": user_text}
        ]
        raw =  self.llm.ask_gpt(messages)

        try:
            start = raw.find('{')
            end = raw.rfind('}') + 1
            j = raw[start:end]
            result = json.loads(j)
            return result
        except Exception as e:
            logger.warning("Failed parse LLM output for intent: %s", e)
            return {
                "intent": "ambiguous",
                "confidence": 0.4,
                "explanation": "llm_response_parse_failed",
                "recommended_action": "ask_clarification",
                "normalized_input": cleaned_text,
            }

    def validate(self, user_input: str):
        cleaned = self.preprocess_text(user_input)
        patterns = self.get_detected_patterns(cleaned)

        if self.detect_injection(cleaned):
            intent = self.ask_intent_llm(cleaned, patterns)
            return {"cleaned": cleaned, "patterns": patterns, "intent": intent}

        return {"cleaned": cleaned, "patterns": patterns, "intent": None}