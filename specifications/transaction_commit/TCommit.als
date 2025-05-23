abstract sig RMState {}
one sig RMWorking, RMPrepared, RMCommitted, RMAborted extends RMState {}

sig RM {
	var state: set RMState
}

pred TCInit {
	all rm : RM | rm.state = RMWorking
}

pred canCommit {
	all rm: RM | rm.state in (RMPrepared + RMCommitted)
}

pred notCommited {
	all rm: RM | rm.state != RMCommitted 
}

pred Prepare[rm: RM] {
	rm.state = RMWorking
	rm.state' = RMPrepared
	all rm2 : RM - rm | rm2.state' = rm2.state
}

pred Decide[rm: RM] {
	{ 
		rm.state = RMPrepared
		canCommit
		rm.state' = RMCommitted
		all rm2 : RM - rm | rm2.state' = rm2.state
	} or {
		rm.state in (RMWorking + RMPrepared)
		notCommited
		rm.state' = RMAborted
		all rm2 : RM - rm | rm2.state' = rm2.state
	}
}

pred TCNext {
	some rm : RM | Prepare[rm] or Decide[rm]
}

pred Fairness {
	always eventually TCNext
}

pred stuttering {
	all rm : RM | rm.state' = rm.state
}

fact TCSpec {
	TCInit
	always (TCNext or stuttering)
	Fairness
}

pred TCConsistent {
	all rm1, rm2 : RM {
		not {
			rm1.state = RMAborted
			rm2.state = RMCommitted
		}
	}
}

check {
	TCConsistent
} for 1.. steps
