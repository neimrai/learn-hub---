import re

def is_question(text):
    # return re.search(r'\b(what|who|where|why|how)\b', text, re.IGNORECASE) is not None or text.strip().endswith('?')
    return re.search(r'\b(what|who|where|why|how)\b', text, re.IGNORECASE) is not None or '?' in text

# 示例
print(is_question("How are you?"))  # True
print(is_question("🥺 Can you reply to this message? 😭"))  # False
