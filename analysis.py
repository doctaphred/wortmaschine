from collections import Counter, namedtuple
from itertools import chain, islice, tee
import random
import re


Token = namedtuple('Token', ['type', 'value'])

word_patterns = re.compile('|'.join([
    r'(?P<VOWEL>[aeiouAEIOU]+)',
    r'(?P<CONSONANT>[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]+)',
    r"(?P<PUNCTUATION>[-'])",
    r'(?P<WHITESPACE>\s+)',
    r'(?P<OTHER>.+)'
]))


def tokenize(word):
    """Split the word into Tokens."""
    scanner = word_patterns.scanner(word)
    for m in iter(scanner.match, None):
        yield Token(m.lastgroup, m.group())


def split(word):
    """Split the word into groups of characters corresponding to tokens."""
    scanner = word_patterns.scanner(word)
    return [m.group() for m in iter(scanner.match, None)]


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ...

    Source: http://docs.python.org/3/library/itertools.html#recipes
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def nth(iterable, n, default=None):
    """Return the nth item or a default value.

    Source: http://docs.python.org/3/library/itertools.html#recipes
    """
    return next(islice(iterable, n, None), default)


def pad(iterable, padding=None):
    """Pad the given iterable with the padding element before and after."""
    yield padding
    yield from iterable
    yield padding


def weighted_choice(counter):
    """Select an element with probability proportional to its frequency."""
    return nth(counter.elements(), random.randrange(sum(counter.values())))


def count_transitions(iterable):
    """Return a Counter of consecutive pairs of elements in iterable."""
    return Counter(pairwise(iterable))


def extract_transitions(transition_counts, start):
    """Return a Counter of transition end values from the given start value."""
    return Counter({b: count for (a, b), count in transition_counts.items()
                    if a == start})


def map_transitions(transition_counts):
    """Return a dict mapping start values to Counters of their end values."""
    start_values = {start for start, end in transition_counts}
    return {start: extract_transitions(transition_counts, start)
            for start in start_values}


def analyze_word(word):
    """Apply count_transitions and map_transitions to the given word."""
    return map_transitions(count_transitions(pad(split(word))))


def analyze_words(words):
    """Apply map_transitions to the given words."""
    transitions = (pairwise(pad(split(word))) for word in words)
    return map_transitions(Counter(chain(*transitions)))


def make_word(transitions):
    """Randomly follow transitions from a word start to a word end.

    transitions should be a mapping from states to Counters of subsequent
    states' frequencies, with the starting and ending states represented as
    None. The first state is determined by selecting a transition from the
    None state, and the process ends when the None state is selected from a
    transition. All selections are made proportionately to their frequencies.

    Example: given a transition map of the word 'banana':

        {None: Counter({'b': 1}),
         'b': Counter({'a': 1}),
         'a': Counter({'n': 2, None: 1}),
         'n': Counter({'a': 2})}

    this function might follow the path

        None -> b -> a -> n -> a -> n -> a -> n -> a -> None

    and return the list

        ['b', 'a', 'n', 'a', 'n', 'a', 'n', 'a']

    This is basically just a quick and dirty Markov chain.
    """
    word = []
    letter_group = weighted_choice(transitions[None])
    while letter_group is not None:
        word.append(letter_group)
        letter_group = weighted_choice(transitions[letter_group])
    return word


if __name__ == '__main__':
    with open('top10000en.txt') as f:
        words = [line.strip() for line in f]

    transitions = analyze_words(words)
    for _ in range(100):
        print(''.join(make_word(transitions)))
