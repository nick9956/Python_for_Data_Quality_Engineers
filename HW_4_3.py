import re


# Copy the text to a variable
def get_text():
    return """
homEwork:
 tHis iz your homeWork, copy these Text to variable.

You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.

last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
"""


# Normalize the text in terms of letter cases
def normalize_text_case(text):
    """
    Converts the entire text to lowercase and capitalizes the first
    letter of each sentence.
    """
    sentences = text.replace('?', '.').replace('!', '.').split('.')
    corrected_sentences = [sentence.strip().capitalize() for sentence in sentences if sentence.strip()]
    return corrected_sentences


# Create a sentence with the last words of each existing sentence and add it to the end of the paragraph
def create_sentence_with_last_words(sentences):
    """
    Creates a new sentence using the last word of each sentence.
    Capitalizes the sentence and adds a period at the end.
    """
    last_words = [sentence.split()[-1] for sentence in sentences]
    return ' '.join(last_words).capitalize() + '.'


# Fix the misspelling "iz" to "is" but only when it is a mistake
def correct_misspelling(sentences):
    """
    Corrects the misspelling of 'iz' with 'is' only when it makes sense.
    Handles cases where 'iz' is surrounded by punctuation.
    """
    sentences = [
        re.sub(r'\biz\b', 'is', re.sub(r'(?<=\w)“iz”', ' “is”', sentence)) for sentence in sentences
    ]
    return sentences


# Calculate the number of whitespace characters in the text
def count_whitespace_characters(text):
    """
    Counts all whitespace characters in the given text.
    """
    return sum(1 for char in text if char.isspace())


# Main function to execute all steps
def process_text():
    """
    Orchestrates the entire text processing pipeline.
    """
    # Get text
    text = get_text()

    # Normalize letter cases
    sentences = normalize_text_case(text)

    # Fix misspellings
    corrected_sentences = correct_misspelling(sentences)

    # Add new sentence with last words
    new_sentence = create_sentence_with_last_words(corrected_sentences)
    normalized_text = '. '.join(corrected_sentences) + '. ' + new_sentence

    # Calculate whitespace characters
    whitespace_count = count_whitespace_characters(normalized_text)

    return normalized_text, whitespace_count


# Process the text
if __name__ == "__main__":
    final_text, whitespace_count = process_text()

    # Print results
    print("Normalized Text:\n")
    print(final_text)
    print("\nNumber of whitespace characters:", whitespace_count)
