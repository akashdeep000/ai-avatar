import re
from typing import List, Tuple
import pysbd
from langdetect import detect

# Constants for additional checks
COMMAS = [
    ",", "،", "，", "、", "፣", "၊", ";", "΄", "‛", "।", "﹐", "꓾", "⹁", "︐", "﹑", "､", "،",
]

END_PUNCTUATIONS = [".", "!", "?", "。", "！", "？", "...", "。。。"]
ABBREVIATIONS = [
    "Mr.", "Mrs.", "Dr.", "Prof.", "Inc.", "Ltd.", "Jr.", "Sr.", "e.g.", "i.e.", "vs.", "St.", "Rd.", "Dr.",
]

# Set of languages directly supported by pysbd
SUPPORTED_LANGUAGES = {
    "am", "ar", "bg", "da", "de", "el", "en", "es", "fa", "fr", "hi", "hy", "it", "ja", "kk", "mr", "my", "nl", "pl", "ru", "sk", "ur", "zh",
}

def detect_language(text: str) -> str:
    """
    Detect text language and check if it's supported by pysbd.
    Returns None for unsupported languages.
    """
    try:
        detected = detect(text)
        return detected if detected in SUPPORTED_LANGUAGES else "en"
    except:
        return "en"

def is_complete_sentence(text: str) -> bool:
    """
    Check if text ends with sentence-ending punctuation and not abbreviation.
    """
    text = text.strip()
    if not text:
        return False
    if any(text.endswith(abbrev) for abbrev in ABBREVIATIONS):
        return False
    return any(text.endswith(punct) for punct in END_PUNCTUATIONS)

def segment_text_by_pysbd(text: str) -> Tuple[List[str], str]:
    """
    Segment text into complete sentences and remaining text.
    """
    if not text:
        return [], ""
    try:
        lang = detect_language(text)
        segmenter = pysbd.Segmenter(language=lang, clean=False)
        sentences = segmenter.segment(text)
        if not sentences:
            return [], text

        complete_sentences = []
        for sent in sentences[:-1]:
            sent = sent.strip()
            if sent:
                complete_sentences.append(sent)

        last_sent = sentences[-1].strip()
        if is_complete_sentence(last_sent):
            complete_sentences.append(last_sent)
            remaining = ""
        else:
            remaining = last_sent
        return complete_sentences, remaining
    except Exception as e:
        # Fallback to regex on any error
        return segment_text_by_regex(text)

def segment_text_by_regex(text: str) -> Tuple[List[str], str]:
    """
    Segment text into complete sentences using regex pattern matching.
    """
    if not text:
        return [], ""
    complete_sentences = []
    remaining_text = text.strip()
    escaped_punctuations = [re.escape(p) for p in END_PUNCTUATIONS]
    pattern = r"(.*?(?:[" + "|".join(escaped_punctuations) + r"]))"
    while remaining_text:
        match = re.search(pattern, remaining_text)
        if not match:
            break
        end_pos = match.end(1)
        potential_sentence = remaining_text[:end_pos].strip()
        if any(potential_sentence.endswith(abbrev) for abbrev in ABBREVIATIONS):
            remaining_text = remaining_text[end_pos:].lstrip()
            continue
        complete_sentences.append(potential_sentence)
        remaining_text = remaining_text[end_pos:].lstrip()
    return complete_sentences, remaining_text

def split_by_comma(sentence: str) -> List[str]:
    """
    Split a sentence by the first comma if it exists.
    """
    for comma in COMMAS:
        if comma in sentence:
            parts = sentence.split(comma, 1)
            return [parts[0] + comma, parts[1].strip()]
    return [sentence]

def split_sentences(text: str, faster_first_response: bool = True) -> List[str]:
    """
    Split text into sentences.
    If faster_first_response is True, it will split the first sentence at a comma.
    """
    complete, remaining = segment_text_by_pysbd(text)

    if faster_first_response and complete:
        first_sentence_parts = split_by_comma(complete[0])
        if len(first_sentence_parts) > 1:
            complete = first_sentence_parts + complete[1:]

    if remaining:
        return complete + [remaining]
    return complete