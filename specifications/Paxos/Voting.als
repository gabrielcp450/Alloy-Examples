open util/ordering[Ballot]

abstract sig Ballot {}

abstract sig Value {}

sig Acceptor {
    var votes: Ballot -> Value,
    var maxBal: lone Ballot
}

sig Quorum {
    nodes: set Acceptor
}

fact QuorumAssumption {
    Quorum.nodes in Acceptor
    all Q1, Q2 : Quorum | some Q1 & Q2
}

pred QuorumNonEmpty {
    all Q : Quorum | some Q
}

pred VotedFor[a: Acceptor, b: Ballot, v: Value] {
    b->v in a.votes
}

pred ChosenAt[b: Ballot, v: Value] {
    some Q : Quorum  { all a : Q.nodes | VotedFor[a, b, v] }
}

fun chosen: set Value {
    {v: Value | (some b: Ballot | ChosenAt[b, v])}
}

pred DidNotVoteAt[a: Acceptor, b: Ballot] {
    all v : Value | not VotedFor[a, b, v]
}

pred CannotVoteAt[a: Acceptor, b: Ballot] {
	lt[b, a.maxBal]
	DidNotVoteAt[a, b]

}

pred NoneOtherChoosableAt[b: Ballot, v: Value] {
    some Q : Quorum {
		all a : Q.nodes | VotedFor[a, b, v] or CannotVoteAt[a, b]
    }
}

pred SafeAt[b: Ballot, v : Value] {
    all c : prevs[b] | NoneOtherChoosableAt[c, v]
}


pred VotesSafe {
    all a : Acceptor, b : Ballot, v : Value | VotedFor[a,b,v] implies SafeAt[b, v]
}

pred OneVote {
    all a : Acceptor, b : Ballot, v, w : Value |
    VotedFor[a, b, v] and VotedFor[a, b, w] implies v = w
}

pred OneValuePerBallot {
    all a1, a2 : Acceptor, b : Ballot, v1, v2 : Value {
        (VotedFor[a1, b, v1] and VotedFor[a2, b, v2]) implies (v1 = v2)
    }
}

pred ShowsSafeAt[Q: Quorum, b: Ballot, v: Value] {
	some Q.nodes
    all a : (Q.nodes) | gte[a.maxBal, b]

    // or theres no votes for ballots smaller than b
    // or theres some vote but no more after
	(all d: prevs[b], a: Q.nodes | DidNotVoteAt[a, d]) or (
        some c: prevs[b] {
            some a: Q.nodes | VotedFor[a, c, v]
            all d: nexts[c] - nexts[b.prev], a: Q.nodes | DidNotVoteAt[a, d]
        } 
    )
}

pred Init {
    no votes
    no maxBal
}

pred IncreaseMaxBal[a: Acceptor, b: Ballot] {
	lt[a.maxBal, b]
    maxBal' = maxBal ++ a->b
    votes' = votes
}

pred VoteFor[a: Acceptor, b: Ballot, v: Value] {
	lte[a.maxBal, b]
	no b.(a.votes)
	all vt : (Acceptor - a).votes {
		(some b.vt) implies b.vt = v
	}
	some Q : Quorum | ShowsSafeAt[Q, b, v]
	votes' = votes ++ a->(a.votes + b->v)
	maxBal' = maxBal ++ (a->b)
}

pred Next {
    some a : Acceptor, b : Ballot { 
		IncreaseMaxBal[a, b] or some v : Value { VoteFor[a, b, v] }
	}
}

pred Fairness {
	always eventually Next
}

pred stuttering {
	votes' = votes
	maxBal' = maxBal
}

fact Spec {
	Init
	always (Next or stuttering)
}

pred Inv {
    VotesSafe implies OneValuePerBallot
}

check {OneValuePerBallot implies OneVote} for 1.. steps
