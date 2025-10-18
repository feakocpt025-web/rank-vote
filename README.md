# RankVote: Instant Runoff Voting System

A Python implementation of ranked-choice voting (also known as instant runoff voting), where voters rank candidates by preference and winners are determined through elimination rounds until someone achieves a majority.

## Overview

RankVote implements the instant runoff voting algorithm used in real-world elections around the globe. Unlike traditional plurality voting where voters choose only one candidate, ranked-choice voting allows voters to express their full preference order. If no candidate receives a majority of first-choice votes, the candidate with the fewest votes is eliminated and their votes are redistributed to the next preference on each ballot. This process continues until a candidate achieves a majority.

## How It Works

1. **Voters rank candidates** from most preferred to least preferred
2. **First-choice votes are counted** - if someone has >50%, they win immediately
3. **If no majority exists:**
   - The candidate with the fewest votes is eliminated
   - Votes for the eliminated candidate transfer to the next preference on each ballot
   - Repeat until someone achieves a majority

## Example

Consider an election with 5 voters and 3 candidates:

```
Voter 1: Alice > Bob > Charlie
Voter 2: Alice > Charlie > Bob
Voter 3: Bob > Alice > Charlie
Voter 4: Bob > Charlie > Alice
Voter 5: Charlie > Alice > Bob
```

**Round 1:** Alice: 2, Bob: 2, Charlie: 1 (no majority)
- Charlie is eliminated (fewest votes)
- Charlie's vote transfers to Alice (their second choice)

**Round 2:** Alice: 3, Bob: 2
- Alice wins with 3/5 = 60% (majority!)

## Project Structure

```
.
├── rankvote.py           # Main implementation (🚧 Needs completion)
├── test_rankvote.py      # Comprehensive test suite (✅ Complete)
└── README.md             # This file
```

## Contributing

This project is a great opportunity to implement a real-world voting algorithm and practice test-driven development. All tests are written and ordered to guide you through the implementation process step by step.

### Getting Started

1. **Fork and clone this repository**

2. **Install the testing framework**
   ```bash
   pip install colorful-test
   ```

3. **Understand the structure**
   - `rankvote.py` contains the `RankVote` class with 8 methods to implement
   - `test_rankvote.py` contains 26 tests organized in a logical progression
   - Tests are numbered (0-25) to guide you through the implementation journey

4. **Implement the methods**
   
   Work through the methods in this recommended order:
   
   **Phase 1: Setup (Tests 0-1)**
   - The `__init__` method is already done
   - Implement `get_remaining_candidates()` - returns non-eliminated candidates
   
   **Phase 2: Ballots (Tests 2-6)**
   - Implement `add_ballot()` - validate and store voter rankings
   - Must reject invalid ballots (wrong candidates, duplicates, wrong count)
   
   **Phase 3: Counting (Tests 7-9)**
   - Implement `get_vote_counts()` - count first-choice votes
   - Must skip eliminated candidates and count next preference
   
   **Phase 4: Analysis (Tests 10-17)**
   - Implement `has_majority_winner()` - check if anyone has >50% of votes
   - Implement `find_last_place()` - find candidate(s) with fewest votes
   - Implement `is_tie()` - check if candidates have equal vote counts
   
   **Phase 5: Elimination (Tests 18-20)**
   - Implement `eliminate_candidate()` - mark a candidate as eliminated
   
   **Phase 6: Full Election (Tests 21-25)**
   - Implement `run_election()` - the main algorithm that brings it all together
   - Repeatedly check for majority, eliminate last place, until winner found
   - Handle complete ties by raising `ValueError`

5. **Run the tests**
   ```bash
   python3 -m colorful_test test_rankvote.py
   ```
   
   The tests are ordered to walk you through the implementation:
   - Tests 0-1: Initialization
   - Tests 2-6: Adding ballots
   - Tests 7-9: Counting votes
   - Tests 10-14: Finding winners and last place
   - Tests 15-17: Tie detection
   - Tests 18-20: Elimination process
   - Tests 21-25: Full election scenarios

6. **Test as you go**
   
   You don't need to implement everything at once! Implement one method, run the tests, see what passes, then move to the next. The colorful output will guide you.

7. **Submit a Pull Request**
   - Include a clear description of your implementation
   - Ensure all 26 tests pass
   - Your PR should show: `26 passed, 0 failed`

### Implementation Guidelines

- **Do not modify the test file** - tests are complete and correct
- **Follow the method signatures** - tests depend on them
- **Handle all edge cases** - empty lists, ties, invalid input
- **Keep it clean** - readable code is better than clever code
- **Use the docstrings** - each method has detailed documentation
- **Test incrementally** - implement one method, test, repeat

### Method Summary

| Method | Purpose | Key Challenge |
|--------|---------|---------------|
| `get_remaining_candidates()` | Return non-eliminated candidates | Filter the eliminated set |
| `add_ballot()` | Validate and store ballot | Check for duplicates, invalid candidates |
| `get_vote_counts()` | Count first-choice votes | Skip eliminated candidates |
| `has_majority_winner()` | Check for >50% winner | Calculate percentage correctly |
| `find_last_place()` | Find candidate(s) with fewest votes | Handle ties for last place |
| `is_tie()` | Check if candidates have equal votes | Work with any subset |
| `eliminate_candidate()` | Mark candidate as eliminated | Simple but crucial |
| `run_election()` | Run the full algorithm | Combine all methods correctly |

### Testing Your Implementation

```bash
# Run all tests
python3 -m colorful_test test_rankvote.py

# Expected output when complete:
# ✓ 26 passed
# ✓ 0 failed
# ✓ Grade: 100.0%
```

### Try the Program

Once your implementation is complete, you can run actual elections:

```bash
python3 rankvote.py Alice Bob Charlie
```

Example interaction:
```
Number of voters: 5

Candidates: Alice, Bob, Charlie
Rank candidates from most preferred (1) to least preferred.

Voter 1:
  Rank 1: Alice
  Rank 2: Bob
  Rank 3: Charlie

Voter 2:
  Rank 1: Alice
  Rank 2: Charlie
  Rank 3: Bob

...

🎉 Winner: Alice
```

## Algorithm Details

### Majority Definition
A candidate needs **more than 50%** of votes to win (not exactly 50%). With 10 votes, you need at least 6 to win.

### Tie Handling
- **Tie for last place:** Eliminate one arbitrarily (implementation choice)
- **Complete tie (all candidates equal):** Raise `ValueError` - election is undecidable

### Vote Transfer
When a candidate is eliminated, their votes transfer to the next non-eliminated candidate on each ballot. If all remaining preferences are eliminated, that ballot exhausts.

## Real-World Usage

Instant runoff voting is used in:
- Australian federal elections
- Irish presidential elections
- Maine and Alaska state elections (USA)
- Various city elections worldwide
- Academy Awards (Best Picture voting)

## Learning Objectives

By completing this project, you'll practice:
- ✅ **Algorithm implementation** - translating rules into code
- ✅ **Data structure design** - managing complex state
- ✅ **Edge case handling** - ties, eliminations, validation
- ✅ **Test-driven development** - letting tests guide implementation
- ✅ **Python skills** - classes, typing, collections, loops

## Resources

- [Instant Runoff Voting - Wikipedia](https://en.wikipedia.org/wiki/Instant-runoff_voting)
- [Ranked Choice Voting - FairVote](https://www.fairvote.org/rcv)
- [How Ranked Choice Voting Works - CGP Grey (Video)](https://www.youtube.com/watch?v=3Y3jE3B8HsE)

## Questions?

If you have questions about the algorithm, implementation details, or need clarification, feel free to open an issue for discussion.

## License

This project is open source and available for educational purposes.

---

**Ready to get started?** Install colorful-test, implement the methods, and watch those tests turn green! 🚀
