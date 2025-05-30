------------------------------ MODULE MCVoting ------------------------------
EXTENDS Voting, TLC

CONSTANTS a1, a2, a3  \* acceptors
CONSTANTS v1, v2      \* Values

MCAcceptor == {a1, a2, a3}
MCValue == {v1, v2}
MCQuorum == {{a1, a2}, {a1, a3}, {a2, a3}}
MCBallot == 0..1
MCSymmetry == Permutations(MCAcceptor) \cup Permutations(MCValue)
=============================================================================
