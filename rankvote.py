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
        if len(rankings) != len(self.candidates):
            return False  # Invalid ballot if number of rankings is not correct
        if any(c not in self.candidates for c in rankings):
            return False  # Invalid ballot if any candidate is not in the list
        if len(set(rankings)) != len(rankings):
            return False  # Invalid ballot if there are duplicates
        self.ballots.append(rankings)
        return True

    def get_vote_counts(self) -> Dict[str, int]:
        """
        Count current first-choice votes for each non-eliminated candidate.

        Returns:
            Dictionary mapping candidate names to their vote counts
        """
        vote_counts = {candidate: 0 for candidate in self.candidates if candidate not in self.eliminated}
        for ballot in self.ballots:
            # Find the first non-eliminated choice for the ballot
            for choice in ballot:
                if choice not in self.eliminated:
                    vote_counts[choice] += 1
                    break
        return vote_counts

    def has_majority_winner(self) -> Optional[str]:
        """
        Check if any candidate has a majority (> 50%) of votes.

        Returns:
            Name of candidate with majority, or None if no majority
        """
        total_votes = len(self.ballots)
        vote_counts = self.get_vote_counts()
        for candidate, count in vote_counts.items():
            if count > total_votes / 2:
                return candidate
        return None

    def find_last_place(self) -> List[str]:
        """
        Find candidate(s) with the fewest votes.

        Returns:
            List of candidate names tied for last place
        """
        vote_counts = self.get_vote_counts()
        min_votes = min(vote_counts.values()) if vote_counts else 0
        return [candidate for candidate, votes in vote_counts.items() if votes == min_votes]

    def is_tie(self, candidates: List[str]) -> bool:
        """
        Check if given candidates are tied (all have same vote count).

        Args:
            candidates: List of candidate names to check

        Returns:
            True if all candidates have equal votes, False otherwise
        """
        vote_counts = self.get_vote_counts()
        votes = [vote_counts.get(candidate, 0) for candidate in candidates]
        return len(set(votes)) == 1

    def eliminate_candidate(self, candidate: str) -> None:
        """
        Eliminate a candidate from the election.
        Votes for this candidate will transfer to next preference.

        Args:
            candidate: Name of candidate to eliminate
        """
        self.eliminated.add(candidate)

    def get_remaining_candidates(self) -> List[str]:
        """
        Get list of candidates who have not been eliminated.

        Returns:
            List of non-eliminated candidate names
        """
        return [candidate for candidate in self.candidates if candidate not in self.eliminated]

    def run_election(self) -> str:
        """
        Run the instant runoff voting process until a winner is determined.

        Returns:
            Name of the winning candidate

        Raises:
            ValueError: If election ends in a complete tie
        """
        while True:
            # Check for majority winner
            winner = self.has_majority_winner()
            if winner:
                return winner

            # Find the last place candidate(s)
            last_place = self.find_last_place()

            # If there's a tie for last place among all candidates, raise an error
            if len(last_place) == len(self.get_remaining_candidates()):
                raise ValueError("Election ends in a complete tie. No winner.")

            # Eliminate the last place candidate(s) (arbitrarily choose one if there's a tie)
            self.eliminate_candidate(last_place[0])

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

