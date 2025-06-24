import random
import string
import nltk
import re
import difflib
from itertools import permutations
from collections import Counter

nltk.download('words', quiet=True)
from nltk.corpus import words as nltk_words

english_words = set(word.lower() for word in nltk_words.words())

def jumble_text(text):
    # Extract only letters or keep spaces? Here we keep spaces as is
    chars = list(text)
    # Get positions of letters only
    letter_positions = [i for i, c in enumerate(chars) if c.isalpha()]
    letters = [chars[i] for i in letter_positions]

    random.shuffle(letters)

    # Replace letters in original positions with shuffled letters
    for pos, letter in zip(letter_positions, letters):
        chars[pos] = letter

    return ''.join(chars)

def score_jumble(text):
    # Score is the number of valid English words in the text
    words_in_text = re.findall(r'[a-zA-Z]+', text)
    if not words_in_text:
        return 0
    valid = sum(1 for w in words_in_text if w.lower() in english_words)
    return valid

def solve_jumble(ciphertext, max_iterations=100000):
    chars = list(ciphertext)
    letter_positions = [i for i, c in enumerate(chars) if c.isalpha()]
    best_letters = [chars[i] for i in letter_positions]
    best_score = score_jumble(ciphertext)
    best_text = ciphertext
    attempts = 0
    try:
        while attempts < max_iterations:
            i, j = random.sample(range(len(best_letters)), 2)
            new_letters = best_letters[:]
            new_letters[i], new_letters[j] = new_letters[j], new_letters[i]
            candidate_chars = chars[:]
            for pos, letter in zip(letter_positions, new_letters):
                candidate_chars[pos] = letter
            candidate_text = ''.join(candidate_chars)
            score = score_jumble(candidate_text)
            attempts += 1
            # Print progress for every attempt
            preview = candidate_text[:60].replace('\n', ' ')
            print(f"\rAttempt: {attempts} | Score: {score} | Best: {best_score} | Preview: {preview}", end="")
            if score > best_score:
                best_score = score
                best_letters = new_letters
                best_text = candidate_text
                print(f"\n[Improved @ attempt {attempts} | Score: {best_score}]\n{best_text}\n")
            if best_score == len(re.findall(r'[a-zA-Z]+', ciphertext)):
                break
    except KeyboardInterrupt:
        print(f"\nStopped after {attempts} attempts.")
    print(f"\nBest solution found (score: {best_score}, attempts: {attempts}):\n{best_text}")
    return best_text

def solve_jumble_with_plaintext(jumbled, plaintext):
    # Get letter positions for both
    jumbled_chars = list(jumbled)
    plain_chars = list(plaintext)
    jumbled_letter_positions = [i for i, c in enumerate(jumbled_chars) if c.isalpha()]
    plain_letter_positions = [i for i, c in enumerate(plain_chars) if c.isalpha()]
    # Map jumbled letters to plain letters by position
    mapping = {}
    for j_pos, p_pos in zip(jumbled_letter_positions, plain_letter_positions):
        mapping[j_pos] = plain_chars[p_pos]
    # Build solved text
    solved = jumbled_chars[:]
    for pos in mapping:
        solved[pos] = mapping[pos]
    return ''.join(solved)

def partial_jumble_with_hints(plaintext, reveal_fraction=0.4):
    chars = list(plaintext)
    letter_positions = [i for i, c in enumerate(chars) if c.isalpha()]
    n_letters = len(letter_positions)
    n_reveal = int(n_letters * reveal_fraction)
    revealed_indices = set(random.sample(letter_positions, n_reveal))
    # Letters to jumble (not revealed)
    to_jumble_indices = [i for i in letter_positions if i not in revealed_indices]
    to_jumble_letters = [chars[i] for i in to_jumble_indices]
    random.shuffle(to_jumble_letters)
    # Place jumbled letters back, keep revealed in place
    j = 0
    for idx in to_jumble_indices:
        chars[idx] = to_jumble_letters[j]
        j += 1
    return ''.join(chars), revealed_indices

def solve_jumble_with_hints(ciphertext, revealed_indices, plaintext, max_iterations=100000):
    chars = list(ciphertext)
    letter_positions = [i for i, c in enumerate(chars) if c.isalpha()]
    best_letters = [chars[i] for i in letter_positions]
    best_score = score_jumble(ciphertext)
    best_text = ciphertext
    attempts = 0
    try:
        while attempts < max_iterations:
            # Only swap letters that are not revealed
            swappable = [i for i, pos in enumerate(letter_positions) if pos not in revealed_indices]
            if len(swappable) < 2:
                break
            i, j = random.sample(swappable, 2)
            new_letters = best_letters[:]
            new_letters[i], new_letters[j] = new_letters[j], new_letters[i]
            candidate_chars = chars[:]
            for idx, pos in enumerate(letter_positions):
                candidate_chars[pos] = new_letters[idx]
            candidate_text = ''.join(candidate_chars)
            score = score_jumble(candidate_text)
            attempts += 1
            preview = candidate_text[:60].replace('\n', ' ')
            print(f"\rAttempt: {attempts} | Score: {score} | Best: {best_score} | Preview: {preview}", end="")
            if score > best_score:
                best_score = score
                best_letters = new_letters
                best_text = candidate_text
                print(f"\n[Improved @ attempt {attempts} | Score: {best_score}]\n{best_text}\n")
            if best_score == len(re.findall(r'[a-zA-Z]+', ciphertext)):
                break
    except KeyboardInterrupt:
        print(f"\nStopped after {attempts} attempts.")
    print(f"\nBest solution found (score: {best_score}, attempts: {attempts}):\n{best_text}")
    return best_text

def smart_jumble_solver(jumbled_text, max_permutations=5040):
    words = re.findall(r'[a-zA-Z]+', jumbled_text)
    nonword_parts = re.split(r'[a-zA-Z]+', jumbled_text)
    result = []
    for idx, word in enumerate(words):
        word_lower = word.lower()
        candidates = set()
        # For short words, try all permutations
        if len(word) <= 7:
            perms = set(''.join(p) for p in permutations(word_lower))
            candidates = {w for w in perms if w in english_words}
        # For longer words, use difflib to find close matches
        if not candidates:
            close = difflib.get_close_matches(word_lower, english_words, n=3, cutoff=0.7)
            candidates = set(close)
        # Pick the best candidate (or keep the jumbled word if none found)
        if candidates:
            # Prefer the candidate with the highest similarity
            best = max(candidates, key=lambda w: difflib.SequenceMatcher(None, word_lower, w).ratio())
            result.append(best)
        else:
            result.append(word)
        # Add the non-word part after the word
        if idx < len(nonword_parts) - 1:
            result.append(nonword_parts[idx + 1])
    return ''.join(result)

def iterative_smart_jumble_solver(jumbled_text, max_permutations=5040, max_iterations=5):
    """
    Iteratively solve a jumbled sentence by applying found letter constraints to remaining words.
    """
    words = re.findall(r'[a-zA-Z]+', jumbled_text)
    nonword_parts = re.split(r'[a-zA-Z]+', jumbled_text)
    # Track solved words and their positions
    solved = [None] * len(words)
    constraints = [None] * len(words)  # List of lists: for each word, a list of known letters or None
    # Initial pass: try to solve each word independently
    for idx, word in enumerate(words):
        word_lower = word.lower()
        candidates = set()
        if len(word) <= 7:
            perms = set(''.join(p) for p in permutations(word_lower))
            candidates = {w for w in perms if w in english_words}
        if not candidates:
            close = difflib.get_close_matches(word_lower, english_words, n=3, cutoff=0.7)
            candidates = set(close)
        if candidates:
            best = max(candidates, key=lambda w: difflib.SequenceMatcher(None, word_lower, w).ratio())
            solved[idx] = best
            constraints[idx] = list(best)
        else:
            constraints[idx] = [None] * len(word)
    # Iteratively refine using found letters as constraints
    for iteration in range(max_iterations):
        progress = False
        # Build a map of letter positions to known letters across all solved words
        letter_constraints = {}
        for idx, word in enumerate(words):
            if solved[idx]:
                for pos, letter in enumerate(solved[idx]):
                    letter_constraints[(idx, pos)] = letter
        # Try to solve unsolved words using constraints
        for idx, word in enumerate(words):
            if solved[idx]:
                continue
            word_lower = word.lower()
            # Build a pattern with known letters (from constraints)
            pattern = list(word_lower)
            for pos in range(len(word_lower)):
                known = letter_constraints.get((idx, pos))
                if known:
                    pattern[pos] = known
                else:
                    pattern[pos] = None
            # Generate permutations that match the known pattern
            perms = set(''.join(p) for p in permutations(word_lower))
            filtered = set()
            for w in perms:
                if all(pattern[i] is None or w[i] == pattern[i] for i in range(len(w))):
                    filtered.add(w)
            candidates = {w for w in filtered if w in english_words}
            if not candidates:
                close = difflib.get_close_matches(word_lower, english_words, n=3, cutoff=0.7)
                candidates = set(close)
            if candidates:
                best = max(candidates, key=lambda w: difflib.SequenceMatcher(None, word_lower, w).ratio())
                solved[idx] = best
                progress = True
        if not progress:
            break
    # Build the result
    result = []
    for idx, word in enumerate(words):
        if solved[idx]:
            result.append(solved[idx])
        else:
            result.append(word)
        if idx < len(nonword_parts) - 1:
            result.append(nonword_parts[idx + 1])
    return ''.join(result)

def top_letter_overlap_candidates(jumbled_word, wordlist, top_n=5):
    """

        Return the top N words from wordlist with the most letter overlap with jumbled_word,
    and ensure each candidate shares at least one letter with the jumbled word.
    """
    jw_counter = Counter(jumbled_word.lower())
    jw_letters = set(jumbled_word.lower())
    candidates = []
    for w in wordlist:
        if len(w) != len(jumbled_word):
            continue
        w_counter = Counter(w)
        w_letters = set(w)
        # Only consider candidates with at least one letter in common
        if not (jw_letters & w_letters):
            continue
        # Count total matching letters (min count for each letter)
        overlap = sum(min(jw_counter[char], w_counter[char]) for char in jw_counter)
        candidates.append((w, overlap))
    # Sort by overlap (descending), then alphabetically
    candidates.sort(key=lambda x: (-x[1], x[0]))
    return [w for w, _ in candidates[:top_n]]

def interactive_jumble_solver(jumbled_text, top_n=5):
    """
    For each jumbled word, show top N English words by letter overlap and prompt user for a guess.
    """
    words = re.findall(r'[a-zA-Z]+', jumbled_text)
    nonword_parts = re.split(r'[a-zA-Z]+', jumbled_text)
    result = []
    for idx, word in enumerate(words):
        print(f"\nJumbled word: {word}")
        candidates = top_letter_overlap_candidates(word, english_words, top_n=top_n)
        print(f"Top {top_n} candidates by letter overlap:")
        for i, cand in enumerate(candidates, 1):
            print(f"  {i}. {cand}")
        guess = input(f"Enter your guess for '{word}' (or press Enter to skip): ")
        if guess:
            result.append(guess)
        else:
            result.append(word)
        if idx < len(nonword_parts) - 1:
            result.append(nonword_parts[idx + 1])
    print("\nYour constructed sentence:")
    print(''.join(result))
    return ''.join(result)

def guided_interactive_jumble_solver(jumbled_text, max_permutations=100000, top_n=5):
    """
    For each jumbled word, try all permutations (up to max_permutations),
    present the closest English words, and let the user pick the best match.
    Then assemble the sentence and show the result.
    """
    words = re.findall(r'[a-zA-Z]+', jumbled_text)
    nonword_parts = re.split(r'[a-zA-Z]+', jumbled_text)
    result = []
    for idx, word in enumerate(words):
        print(f"\nJumbled word: {word}")
        word_lower = word.lower()
        perms = set()
        # Only generate all permutations if word is short enough
        if len(word) <= 7:
            perms = set(''.join(p) for p in permutations(word_lower))
            if len(perms) > max_permutations:
                perms = set(list(perms)[:max_permutations])
            candidates = [w for w in perms if w in english_words]
        else:
            candidates = []
        # If no valid English word permutations, use difflib to find closest
        if not candidates:
            close = difflib.get_close_matches(word_lower, english_words, n=top_n, cutoff=0.7)
            candidates = close
        # If still none, just use the jumbled word
        if not candidates:
            candidates = [word]
        print(f"Top {top_n} options:")
        for i, cand in enumerate(candidates[:top_n], 1):
            print(f"  {i}. {cand}")
        guess = input(f"Pick the closest word for '{word}' (1-{min(len(candidates), top_n)}) or type your own: ")
        if guess.isdigit() and 1 <= int(guess) <= min(len(candidates), top_n):
            result.append(candidates[int(guess)-1])
        elif guess:
            result.append(guess)
        else:
            result.append(word)
        if idx < len(nonword_parts) - 1:
            result.append(nonword_parts[idx + 1])
    print("\nYour constructed sentence:")
    print(''.join(result))
    return ''.join(result)

def auto_intelligent_jumble_solver(jumbled_text, max_permutations=100000, top_n=5, beam_width=5):
    """
    Automatically and intelligently solve the jumble by maximizing the number of valid English words in the sentence.
    Uses a greedy/beam search approach.
    """
    words = re.findall(r'[a-zA-Z]+', jumbled_text)
    nonword_parts = re.split(r'[a-zA-Z]+', jumbled_text)
    # For each word, get up to top_n candidates (valid permutations or close matches)
    word_candidates = []
    for word in words:
        word_lower = word.lower()
        perms = set()
        if len(word) <= 7:
            perms = set(''.join(p) for p in permutations(word_lower))
            if len(perms) > max_permutations:
                perms = set(list(perms)[:max_permutations])
            candidates = [w for w in perms if w in english_words]
        else:
            candidates = []
        if not candidates:
            close = difflib.get_close_matches(word_lower, english_words, n=top_n, cutoff=0.7)
            candidates = close
        if not candidates:
            candidates = [word]
        word_candidates.append(list(candidates[:top_n]))
    # Beam search: each state is a partial sentence and its score
    from heapq import heappush, heappop
    initial = (0, [])  # (negative score, list of chosen words)
    heap = [initial]
    for idx, candidates in enumerate(word_candidates):
        new_heap = []
        while heap:
            neg_score, chosen = heappop(heap)
            for cand in candidates:
                new_chosen = chosen + [cand]
                # Score: number of valid English words so far
                score = sum(1 for w in new_chosen if w in english_words)
                heappush(new_heap, (-score, new_chosen))
        # Keep only top beam_width states
        heap = sorted(new_heap)[:beam_width]
    # Pick the best result
    best_score, best_words = min(heap)
    # Assemble the sentence
    result = []
    for idx, word in enumerate(best_words):
        result.append(word)
        if idx < len(nonword_parts) - 1:
            result.append(nonword_parts[idx + 1])
    print("\nAuto-intelligent jumble solver result:")
    print(''.join(result))
    print(f"Valid English words in sentence: {-best_score} / {len(words)}")
    return ''.join(result)

def full_sentence_anagram_solver(jumbled_text, min_word_len=2, max_word_len=12, max_results=3, show_progress=True, guesses=None):
    """
    Fully exhaustive multi-word anagram solver with optional user guesses.
    If guesses are provided, they must be included in the solution (if possible).
    """
    from collections import Counter
    import sys
    sys.setrecursionlimit(20000)
    chars = [c for c in jumbled_text if c.isalpha()]
    letter_count = Counter(c.lower() for c in chars)
    total_letters = sum(letter_count.values())
    # Precompute all English words that can be made from the available letters and are within length limits
    possible_words = []
    for w in english_words:
        if min_word_len <= len(w) <= max_word_len:
            wc = Counter(w)
            if all(wc[char] <= letter_count.get(char, 0) for char in wc):
                possible_words.append(w)
    # Sort by length descending for efficiency
    possible_words.sort(key=lambda w: -len(w))
    results = []
    seen = set()
    progress = {'calls': 0, 'found': 0}
    # If guesses not provided, prompt user
    if guesses is None:
        guess_input = input("Enter your guess for any word(s) (comma separated, or leave blank for none): ").strip()
        if guess_input:
            guesses = [g.strip().lower() for g in guess_input.split(',') if g.strip()]
        else:
            guesses = []
    # Check if guesses are possible
    working_letter_count = letter_count.copy()
    for guess in guesses:
        gc = Counter(guess)
        if not all(gc[c] <= working_letter_count.get(c, 0) for c in gc):
            print(f"Guess '{guess}' cannot be formed from the available letters. Skipping this guess.")
            guesses = [g for g in guesses if g != guess]
        else:
            for c in gc:
                working_letter_count[c] -= gc[c]
    def backtrack(remaining, path):
        progress['calls'] += 1
        if show_progress and progress['calls'] % 10000 == 0:
            print(f"Tried {progress['calls']} paths, found {progress['found']} valid sentences so far...")
        if not remaining:
            # Only accept if all guesses are in the path
            if all(g in path for g in guesses):
                sentence = tuple(sorted(path))
                if sentence not in seen:
                    results.append(path[:])
                    seen.add(sentence)
                    progress['found'] += 1
            return len(results) >= max_results
        for w in possible_words:
            wc = Counter(w)
            if all(remaining.get(c, 0) >= wc[c] for c in wc):
                path.append(w)
                new_remaining = remaining.copy()
                for c in wc:
                    new_remaining[c] -= wc[c]
                if backtrack(new_remaining, path):
                    return True
                path.pop()
        return False
    # Start with guesses in the path
    path = guesses[:]
    backtrack(working_letter_count, path)
    if not results:
        print("No full anagram sentence found.")
        return None
    for idx, best in enumerate(results):
        sentence = ' '.join(best)
        print(f"\nFull sentence anagram solver result #{idx+1}:")
        print(sentence)
    return [' '.join(best) for best in results]

if __name__ == "__main__":
    plaintext = "This is a simple text jumbling cipher for you to solve."
    ciphertext = jumble_text(plaintext)
    print("Plaintext:")
    print(plaintext)
    print("\nJumbled ciphertext:")
    print(ciphertext)
    print("\nSuper smart NLTK-based solution:")
    print(smart_jumble_solver(ciphertext))
    print("\nIterative smart jumble solver (with constraint propagation):")
    print(iterative_smart_jumble_solver(ciphertext))
    print("\nSolving the jumble with known plaintext...")
    solved = solve_jumble_with_plaintext(ciphertext, plaintext)
    print("\nSolved:")
    print(solved)
    partial_ciphertext, revealed_indices = partial_jumble_with_hints(plaintext, reveal_fraction=0.4)
    print("\nPartially jumbled ciphertext (40% revealed):")
    print(partial_ciphertext)
    print("\nSolving the jumble with 40% hints...")
    solve_jumble_with_hints(partial_ciphertext, revealed_indices, plaintext)
    print("\nInteractive jumble solver (top 5 letter-overlap candidates and guess box):")
    interactive_jumble_solver(ciphertext, top_n=5)
    print("\nGuided interactive jumble solver (all options, user picks closest):")
    guided_interactive_jumble_solver(ciphertext, max_permutations=100000, top_n=5)
    print("\nAuto-intelligent jumble solver (no user input, maximizes valid words):")
    auto_intelligent_jumble_solver(ciphertext, max_permutations=100000, top_n=5, beam_width=5)
    print("\nFull sentence anagram solver (fully exhaustive, all valid sentences, with guess option):")
    full_sentence_anagram_solver(ciphertext)
