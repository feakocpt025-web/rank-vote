"""
Tests for RankVote: Instant Runoff Voting System

Tests are ordered to walk through the implementation journey:
1. Initialization and setup
2. Adding and validating ballots
3. Counting votes
4. Finding winners and last place
5. Elimination process
6. Full election scenarios
"""

from colorful_test import TestCase, show_message
from rankvote import RankVote


class TestRankVote(TestCase):

    # =====================
    # STEP 1: INITIALIZATION (Test First)
    # =====================

    @show_message(
        success="Election initializes with candidates correctly",
        fail="Failed to initialize election with candidates.\nExpected: %f\nReceived: %f",
    )
    def test_initialization_0(self):
        """Test that election can be created with candidates."""
        election = RankVote(["Alice", "Bob", "Charlie"])
        self.assert_equal(election.candidates, ["Alice", "Bob", "Charlie"])
        self.assert_equal(len(election.ballots), 0)
        self.assert_equal(len(election.eliminated), 0)

    @show_message(
        success="Get remaining candidates works initially",
        fail="Failed to get initial remaining candidates.\nExpected: %f\nReceived: %f",
    )
    def test_get_remaining_candidates_initial_1(self):
        """Test getting remaining candidates at start (all candidates)."""
        election = RankVote(["Alice", "Bob", "Charlie"])
        remaining = election.get_remaining_candidates()
        self.assert_equal(set(remaining), {"Alice", "Bob", "Charlie"})

    # =====================
    # STEP 2: ADDING BALLOTS
    # =====================

    @show_message(
        success="Valid ballot is accepted and stored",
        fail="Failed to add valid ballot.\nExpected ballot to be added",
    )
    def test_add_valid_ballot_2(self):
        """Test adding a valid ballot."""
        election = RankVote(["Alice", "Bob", "Charlie"])
        result = election.add_ballot(["Alice", "Bob", "Charlie"])
        self.assert_equal(result, True)
        self.assert_equal(len(election.ballots), 1)

    @show_message(
        success="Multiple ballots can be added",
        fail="Failed to add multiple ballots.\nExpected: %f ballots\nReceived: %f",
    )
    def test_add_multiple_ballots_3(self):
        """Test adding multiple valid ballots."""
        election = RankVote(["Alice", "Bob", "Charlie"])
        election.add_ballot(["Alice", "Bob", "Charlie"])
        election.add_ballot(["Bob", "Alice", "Charlie"])
        election.add_ballot(["Charlie", "Bob", "Alice"])
        self.assert_equal(len(election.ballots), 3)

    @show_message(
        success="Invalid ballot (wrong candidate) is rejected",
        fail="Should reject ballot with invalid candidate.\nExpected: False",
    )
    def test_add_invalid_ballot_candidate_4(self):
        """Test that ballot with non-existent candidate is rejected."""
        election = RankVote(["Alice", "Bob", "Charlie"])
        result = election.add_ballot(["Alice", "Bob", "David"])
        self.assert_equal(result, False)
        self.assert_equal(len(election.ballots), 0)

    @show_message(
        success="Invalid ballot (duplicate candidate) is rejected",
        fail="Should reject ballot with duplicate candidates.\nExpected: False",
    )
    def test_add_invalid_ballot_duplicate_5(self):
        """Test that ballot with duplicate rankings is rejected."""
        election = RankVote(["Alice", "Bob", "Charlie"])
        result = election.add_ballot(["Alice", "Alice", "Bob"])
        self.assert_equal(result, False)
        self.assert_equal(len(election.ballots), 0)

    @show_message(
        success="Invalid ballot (wrong count) is rejected",
        fail="Should reject ballot with wrong number of candidates.\nExpected: False",
    )
    def test_add_invalid_ballot_count_6(self):
        """Test that ballot with wrong number of candidates is rejected."""
        election = RankVote(["Alice", "Bob", "Charlie"])
        result = election.add_ballot(["Alice", "Bob"])
        self.assert_equal(result, False)
        self.assert_equal(len(election.ballots), 0)

    # =====================
    # STEP 3: COUNTING VOTES
    # =====================

    @show_message(
        success="Vote counting works with simple ballots",
        fail="Failed to count first-choice votes correctly.\nExpected: %s\nReceived: %f",
    )
    def test_get_vote_counts_simple_7(self):
        """Test counting first-choice votes."""
        election = RankVote(["Alice", "Bob", "Charlie"])
        election.add_ballot(["Alice", "Bob", "Charlie"])
        election.add_ballot(["Alice", "Charlie", "Bob"])
        election.add_ballot(["Bob", "Alice", "Charlie"])

        counts = election.get_vote_counts()
        self.assert_equal(counts["Alice"], 2)
        self.assert_equal(counts["Bob"], 1)
        self.assert_equal(counts["Charlie"], 0)

    @show_message(
        success="Vote counting works with all candidates receiving votes",
        fail="Failed to count votes when all candidates have votes.\nExpected: %s\nReceived: %f",
    )
    def test_get_vote_counts_all_candidates_8(self):
        """Test vote counting when all candidates have votes."""
        election = RankVote(["Alice", "Bob", "Charlie"])
        election.add_ballot(["Alice", "Bob", "Charlie"])
        election.add_ballot(["Bob", "Alice", "Charlie"])
        election.add_ballot(["Charlie", "Alice", "Bob"])

        counts = election.get_vote_counts()
        self.assert_equal(counts["Alice"], 1)
        self.assert_equal(counts["Bob"], 1)
        self.assert_equal(counts["Charlie"], 1)

    @show_message(
        success="Vote counting ignores eliminated candidates",
        fail="Should count votes for next preference after elimination.\nExpected: %s\nReceived: %f",
    )
    def test_get_vote_counts_with_elimination_9(self):
        """Test that vote counting skips eliminated candidates."""
        election = RankVote(["Alice", "Bob", "Charlie"])
        election.add_ballot(["Charlie", "Alice", "Bob"])
        election.add_ballot(["Charlie", "Bob", "Alice"])
        election.add_ballot(["Bob", "Alice", "Charlie"])

        # Eliminate Charlie
        election.eliminate_candidate("Charlie")

        # Now Charlie's votes should transfer to next choice
        counts = election.get_vote_counts()
        self.assert_equal(counts["Alice"], 1)  # From first ballot
        self.assert_equal(counts["Bob"], 2)  # Original 1 + 1 from second ballot

    # =====================
    # STEP 4: FINDING WINNERS AND LAST PLACE
    # =====================

    @show_message(
        success="Majority winner detected correctly (clear majority)",
        fail="Failed to detect candidate with majority.\nExpected: %s\nReceived: %f",
    )
    def test_has_majority_winner_clear_10(self):
        """Test detecting a clear majority winner."""
        election = RankVote(["Alice", "Bob", "Charlie"])
        election.add_ballot(["Alice", "Bob", "Charlie"])
        election.add_ballot(["Alice", "Charlie", "Bob"])
        election.add_ballot(["Alice", "Bob", "Charlie"])
        election.add_ballot(["Bob", "Alice", "Charlie"])
        election.add_ballot(["Bob", "Charlie", "Alice"])

        # Alice has 3/5 = 60% (majority)
        winner = election.has_majority_winner()
        self.assert_equal(winner, "Alice")

    @show_message(
        success="No majority winner returns None",
        fail="Should return None when no candidate has majority.\nExpected: None\nReceived: %f",
    )
    def test_has_majority_no_winner_11(self):
        """Test that None is returned when no majority exists."""
        election = RankVote(["Alice", "Bob", "Charlie"])
        election.add_ballot(["Alice", "Bob", "Charlie"])
        election.add_ballot(["Bob", "Alice", "Charlie"])
        election.add_ballot(["Charlie", "Bob", "Alice"])

        # Each has 1/3 = 33% (no majority)
        winner = election.has_majority_winner()
        self.assert_equal(winner, None)

    @show_message(
        success="Exact 50% is not a majority",
        fail="50% should NOT be a majority (need > 50%).\nExpected: None\nReceived: %f",
    )
    def test_has_majority_exactly_half_12(self):
        """Test that exactly 50% is not considered a majority."""
        election = RankVote(["Alice", "Bob"])
        election.add_ballot(["Alice", "Bob"])
        election.add_ballot(["Bob", "Alice"])

        # Each has 1/2 = 50% (not majority, need > 50%)
        winner = election.has_majority_winner()
        self.assert_equal(winner, None)

    @show_message(
        success="Find last place candidate works correctly",
        fail="Failed to identify candidate with fewest votes.\nExpected: %s\nReceived: %f",
    )
    def test_find_last_place_single_13(self):
        """Test finding single candidate in last place."""
        election = RankVote(["Alice", "Bob", "Charlie"])
        election.add_ballot(["Alice", "Bob", "Charlie"])
        election.add_ballot(["Alice", "Charlie", "Bob"])
        election.add_ballot(["Bob", "Alice", "Charlie"])

        # Charlie has 0 votes (last place)
        last_place = election.find_last_place()
        self.assert_equal(last_place, ["Charlie"])

    @show_message(
        success="Find last place handles ties correctly",
        fail="Failed to identify multiple candidates tied for last.\nExpected: %s\nReceived: %f",
    )
    def test_find_last_place_tie_14(self):
        """Test finding multiple candidates tied for last place."""
        election = RankVote(["Alice", "Bob", "Charlie", "Diana"])
        election.add_ballot(["Alice", "Bob", "Charlie", "Diana"])
        election.add_ballot(["Alice", "Bob", "Diana", "Charlie"])
        election.add_ballot(["Bob", "Alice", "Charlie", "Diana"])
        election.add_ballot(["Bob", "Alice", "Diana", "Charlie"])

        # Charlie and Diana both have 0 votes
        last_place = election.find_last_place()
        self.assert_equal(set(last_place), {"Charlie", "Diana"})

    # =====================
    # STEP 5: TIE DETECTION
    # =====================

    @show_message(
        success="Tie detection works for actual tie",
        fail="Failed to detect tie among candidates.\nExpected: True\nReceived: %f",
    )
    def test_is_tie_true_15(self):
        """Test detecting when candidates are tied."""
        election = RankVote(["Alice", "Bob", "Charlie"])
        election.add_ballot(["Alice", "Bob", "Charlie"])
        election.add_ballot(["Bob", "Charlie", "Alice"])
        election.add_ballot(["Charlie", "Alice", "Bob"])

        # All have 1 vote (tie)
        is_tied = election.is_tie(["Alice", "Bob", "Charlie"])
        self.assert_equal(is_tied, True)

    @show_message(
        success="Tie detection returns False when not tied",
        fail="Should return False when candidates have different vote counts.\nExpected: False\nReceived: %f",
    )
    def test_is_tie_false_16(self):
        """Test detecting when candidates are not tied."""
        election = RankVote(["Alice", "Bob", "Charlie"])
        election.add_ballot(["Alice", "Bob", "Charlie"])
        election.add_ballot(["Alice", "Charlie", "Bob"])
        election.add_ballot(["Bob", "Charlie", "Alice"])

        # Alice: 2, Bob: 1, Charlie: 0 (not tied)
        is_tied = election.is_tie(["Alice", "Bob", "Charlie"])
        self.assert_equal(is_tied, False)

    @show_message(
        success="Tie detection works for subset of candidates",
        fail="Failed to detect tie among subset of candidates.\nExpected: True\nReceived: %f",
    )
    def test_is_tie_subset_17(self):
        """Test tie detection for subset of candidates."""
        election = RankVote(["Alice", "Bob", "Charlie"])
        election.add_ballot(["Alice", "Bob", "Charlie"])
        election.add_ballot(["Bob", "Charlie", "Alice"])
        election.add_ballot(["Charlie", "Alice", "Bob"])

        # Bob and Charlie both have 1 vote (tied)
        is_tied = election.is_tie(["Bob", "Charlie"])
        self.assert_equal(is_tied, True)

    # =====================
    # STEP 6: ELIMINATION PROCESS
    # =====================

    @show_message(
        success="Candidate elimination works",
        fail="Failed to eliminate candidate.\nExpected candidate to be in eliminated set",
    )
    def test_eliminate_candidate_18(self):
        """Test eliminating a candidate."""
        election = RankVote(["Alice", "Bob", "Charlie"])
        election.eliminate_candidate("Charlie")

        assert "Charlie" in election.eliminated
        self.assert_equal(len(election.eliminated), 1)

    @show_message(
        success="Remaining candidates updates after elimination",
        fail="get_remaining_candidates should exclude eliminated candidates.\nExpected: %s\nReceived: %f",
    )
    def test_get_remaining_after_elimination_19(self):
        """Test that eliminated candidates are not in remaining list."""
        election = RankVote(["Alice", "Bob", "Charlie"])
        election.eliminate_candidate("Charlie")

        remaining = election.get_remaining_candidates()
        self.assert_equal(set(remaining), {"Alice", "Bob"})

    @show_message(
        success="Multiple eliminations work correctly",
        fail="Failed to handle multiple eliminations.\nExpected: %s\nReceived: %f",
    )
    def test_multiple_eliminations_20(self):
        """Test eliminating multiple candidates."""
        election = RankVote(["Alice", "Bob", "Charlie", "Diana"])
        election.eliminate_candidate("Charlie")
        election.eliminate_candidate("Diana")

        remaining = election.get_remaining_candidates()
        self.assert_equal(set(remaining), {"Alice", "Bob"})
        self.assert_equal(len(election.eliminated), 2)

    # =====================
    # STEP 7: FULL ELECTION SCENARIOS
    # =====================

    @show_message(
        success="Election with immediate majority winner works",
        fail="Failed to determine winner when candidate has immediate majority.\nExpected: %s\nReceived: %f",
    )
    def test_run_election_immediate_majority_21(self):
        """Test election where someone wins immediately with majority."""
        election = RankVote(["Alice", "Bob", "Charlie"])
        election.add_ballot(["Alice", "Bob", "Charlie"])
        election.add_ballot(["Alice", "Charlie", "Bob"])
        election.add_ballot(["Alice", "Bob", "Charlie"])
        election.add_ballot(["Bob", "Alice", "Charlie"])
        election.add_ballot(["Bob", "Charlie", "Alice"])

        # Alice has 3/5 = 60% (immediate majority)
        winner = election.run_election()
        self.assert_equal(winner, "Alice")

    @show_message(
        success="Election with runoff elimination works",
        fail="Failed to run elimination rounds correctly.\nExpected: %s\nReceived: %f",
    )
    def test_run_election_with_elimination_22(self):
        """Test election requiring elimination rounds."""
        election = RankVote(["Alice", "Bob", "Charlie"])
        # Round 1: Alice: 2, Bob: 2, Charlie: 1 (no majority, eliminate Charlie)
        election.add_ballot(["Alice", "Bob", "Charlie"])
        election.add_ballot(["Alice", "Charlie", "Bob"])
        election.add_ballot(["Bob", "Alice", "Charlie"])
        election.add_ballot(["Bob", "Charlie", "Alice"])
        election.add_ballot(["Charlie", "Alice", "Bob"])

        # After eliminating Charlie, their vote goes to Alice
        # Round 2: Alice: 3, Bob: 2 (Alice wins with 3/5 = 60%)
        winner = election.run_election()
        self.assert_equal(winner, "Alice")

    @show_message(
        success="Election with multiple elimination rounds works",
        fail="Failed to handle multiple elimination rounds.\nExpected: %s\nReceived: %f",
    )
    def test_run_election_multiple_eliminations_23(self):
        """Test election with multiple elimination rounds."""
        election = RankVote(["Alice", "Bob", "Charlie", "Diana"])
        # Round 1: Alice: 2, Bob: 2, Charlie: 1, Diana: 0
        election.add_ballot(["Alice", "Bob", "Charlie", "Diana"])
        election.add_ballot(["Alice", "Charlie", "Bob", "Diana"])
        election.add_ballot(["Bob", "Alice", "Diana", "Charlie"])
        election.add_ballot(["Bob", "Charlie", "Alice", "Diana"])
        election.add_ballot(["Charlie", "Alice", "Bob", "Diana"])

        # Eliminate Diana first, then Charlie
        # Eventually Alice or Bob should win
        winner = election.run_election()
        assert winner in ["Alice", "Bob"]

    @show_message(
        success="Complete tie raises ValueError",
        fail="Should raise ValueError when election ends in complete tie",
    )
    def test_run_election_complete_tie_24(self):
        """Test that complete tie raises appropriate error."""
        election = RankVote(["Alice", "Bob"])
        election.add_ballot(["Alice", "Bob"])
        election.add_ballot(["Bob", "Alice"])

        # Both have 1/2 = 50% (tie, no one can be eliminated)
        self.assert_raises(ValueError, election.run_election)

    @show_message(
        success="Two-candidate race with clear winner works",
        fail="Failed simple two-candidate election.\nExpected: %s\nReceived: %f",
    )
    def test_run_election_two_candidates_25(self):
        """Test simple two-candidate race."""
        election = RankVote(["Alice", "Bob"])
        election.add_ballot(["Alice", "Bob"])
        election.add_ballot(["Alice", "Bob"])
        election.add_ballot(["Bob", "Alice"])

        # Alice: 2/3 = 67% (majority)
        winner = election.run_election()
        self.assert_equal(winner, "Alice")


if __name__ == "__main__":
    TestRankVote.run_and_output_results()
