"""
RankVote: Instant Runoff Voting System

A program that implements ranked-choice voting (instant runoff voting).
Voters rank candidates by preference, and if no candidate has a majority,
the candidate with fewest votes is eliminated and votes redistributed.
"""

import sys
from typing import List, Dict, Optional, Set


class RankVote:
    """Manages an instant runoff voting election."""

    def __init__(self, candidates: List[str]):
        """
        Initialize election with list of candidates.

        Args:
            candidates: List of candidate names
        """
        self.candidates = candidates
        self.ballots: List[List[str]] = []
        self.eliminated: Set[str] = set()

    def add_ballot(self, rankings: List[str]) -> bool:
        """
        Add a ballot with voter's ranked preferences.

        Args:
            rankings: List of candidate names in order of preference

        Returns:
            True if ballot is valid and added, False otherwise
        """
        pass

    def get_vote_counts(self) -> Dict[str, int]:
        """
        Count current first-choice votes for each non-eliminated candidate.

        Returns:
            Dictionary mapping candidate names to their vote counts
        """
        pass

    def has_majority_winner(self) -> Optional[str]:
        """
        Check if any candidate has a majority (> 50%) of votes.

        Returns:
            Name of candidate with majority, or None if no majority
        """
        pass

    def find_last_place(self) -> List[str]:
        """
        Find candidate(s) with the fewest votes.

        Returns:
            List of candidate names tied for last place
        """
        pass

    def is_tie(self, candidates: List[str]) -> bool:
        """
        Check if given candidates are tied (all have same vote count).

        Args:
            candidates: List of candidate names to check

        Returns:
            True if all candidates have equal votes, False otherwise
        """
        pass

    def eliminate_candidate(self, candidate: str) -> None:
        """
        Eliminate a candidate from the election.
        Votes for this candidate will transfer to next preference.

        Args:
            candidate: Name of candidate to eliminate
        """
        pass

    def get_remaining_candidates(self) -> List[str]:
        """
        Get list of candidates who have not been eliminated.

        Returns:
            List of non-eliminated candidate names
        """
        pass

    def run_election(self) -> str:
        """
        Run the instant runoff voting process until a winner is determined.

        Returns:
            Name of the winning candidate

        Raises:
            ValueError: If election ends in a complete tie
        """
        pass


def main():
    """Main program entry point."""
    # Check command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python rankvote.py candidate1 candidate2 candidate3 ...")
        sys.exit(1)

    # Get candidates from command line
    candidates = sys.argv[1:]

    # Initialize election
    election = RankVote(candidates)

    # Get number of voters
    try:
        num_voters = int(input("Number of voters: "))
    except ValueError:
        print("Invalid number of voters")
        sys.exit(1)

    # Collect ballots
    print(f"\nCandidates: {', '.join(candidates)}")
    print("Rank candidates from most preferred (1) to least preferred.\n")

    for i in range(num_voters):
        print(f"Voter {i + 1}:")
        rankings = []
        for rank in range(len(candidates)):
            while True:
                choice = input(f"  Rank {rank + 1}: ")
                if choice in candidates and choice not in rankings:
                    rankings.append(choice)
                    break
                else:
                    print(f"  Invalid choice. Must be a candidate not already ranked.")

        election.add_ballot(rankings)
        print()

    # Run election and announce winner
    try:
        winner = election.run_election()
        print(f"\n🎉 Winner: {winner}")
    except ValueError as e:
        print(f"\n❌ {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
