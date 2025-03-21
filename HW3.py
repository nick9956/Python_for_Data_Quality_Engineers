import re

# Copy the text to a variable
text = """
homEwork:
 tHis iz your homeWork, copy these Text to variable.

You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.

last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
"""

# Normalize the text in terms of letter cases
text = text.lower()

# Split the text into sentences using `.split('.')` or similar approaches
sentences = text.replace('?', '.').replace('!', '.').split('.')

# Capitalize the first letter of each sentence
corrected_sentences = [sentence.strip().capitalize() for sentence in sentences if sentence.strip()]

# Correct "iz" only when it is a standalone word or clearly a mistake
corrected_sentences = [
    re.sub(r'\biz\b', 'is', re.sub(r'(?<=\w)“iz”', ' “is”', sentence)) for sentence in corrected_sentences
]

# Extract the last word from each sentence
last_words = [sentence.split()[-1] for sentence in corrected_sentences]

# Create a new sentence with the last words and capitalize it
new_sentence = ' '.join(last_words).capitalize() + '.'

# Add the new sentence to the paragraph
normalized_text = '. '.join(corrected_sentences) + '. ' + new_sentence

# Calculate the number of whitespace characters in the text
whitespace_count = sum(1 for char in normalized_text if char.isspace())

print(normalized_text)
print("\nNumber of whitespace characters:", whitespace_count)
