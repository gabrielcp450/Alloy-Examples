abstract sig RMState {}
one sig RMWorking, RMPrepared, RMCommitted, RMAborted extends RMState {}

sig RM {
	var state: one RMState 
}

pred TCInit {
	RM.state = RMWorking 
}

pred canCommit {
	RM.state in (RMPrepared + RMCommitted)
}

pred notCommited {
	RMCommitted not in RM.state
}

pred Prepare[rm: RM] {
	rm.state = RMWorking
	state' = state ++ rm->RMPrepared
}

pred Decide[rm: RM] {
	{ 
		rm.state = RMPrepared
		canCommit
		state' = state ++ rm->RMCommitted
	} or {
		rm.state in (RMWorking + RMPrepared)
		notCommited
		state' = state ++ rm->RMAborted
	}
}

pred TCNext {
	some rm : RM | Prepare[rm] or Decide[rm]
}


pred stuttering {
	state' = state
}

fact TCSpec {
	TCInit
	always (TCNext or stuttering)
}

run AllCommited {
	eventually RM.state = RMCommitted
} for exactly 3 RM

run AllAborted {
	eventually RM.state = RMAborted
} for exactly 3 RM

check TCConsistent {
	always {
		all rm1, rm2 : RM {
			not {
				rm1.state = RMAborted
				rm2.state = RMCommitted
			}
		}
	}
} for exactly 3 RM, 1.. steps
