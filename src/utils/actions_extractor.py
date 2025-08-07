import re
from typing import List, Tuple

def extract_actions(text: str, expression_keys: List[str], motion_keys: List[str]) -> Tuple[str, List[str], List[str]]:
    """
    Extracts expressions and motions from a text string.

    Args:
        text: The text to parse.
        expression_keys: A list of valid expression keywords.
        motion_keys: A list of valid motion keywords.

    Returns:
        A tuple containing the cleaned text, a list of extracted expressions,
        and a list of extracted motions.
    """
    cleaned_text = text
    expressions = []
    motions = []

    # Extract expressions
    if expression_keys:
        exp_pattern = r'\[e:(' + '|'.join(re.escape(key) for key in expression_keys) + r')\]'
        expressions = re.findall(exp_pattern, cleaned_text)
        cleaned_text = re.sub(exp_pattern, '', cleaned_text)

    # Extract motions
    if motion_keys:
        mot_pattern = r'\[m:(' + '|'.join(re.escape(key) for key in motion_keys) + r')\]'
        motions = re.findall(mot_pattern, cleaned_text)
        cleaned_text = re.sub(mot_pattern, '', cleaned_text)

    return cleaned_text.strip(), expressions, motions