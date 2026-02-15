from collections import Counter

def find_repeated_words_raw(headers):
    valid_headers = [h for h in headers if h is not None]
    if not valid_headers:
        return {}
    
    combined = " ".join(valid_headers).lower()
    words = combined.split()
    word_counts = Counter(words)
    return {word: count for word, count in word_counts.items() if count > 2}

def find_repeated_words_semantic(headers):
    valid_headers = [h for h in headers if h is not None]
    if not valid_headers:
        return {}
    
    STOPWORDS = {
    "the", "and", "to", "of", "a", "in", "is", "for",
    "on", "with", "at", "by", "an", "be", "this",
    "that", "from", "as", "it", "are"
}
    
    combined = " ".join(valid_headers).lower()
    words = combined.split()
    filtered_words = [w for w in words if w not in STOPWORDS]
    word_counts = Counter(filtered_words)
    return {word: count for word, count in word_counts.items() if count > 2}





