abstract sig RMState {}
abstract sig TMState {}

one sig RMWorking, RMPrepared, RMCommitted, RMAborted extends RMState {}
one sig TMInit, TMCommitted, TMAborted extends TMState {}


one sig MsgCommit, MsgAbort {}
var sig Msgs in MsgCommit + MsgAbort + RM {}

sig RM {
	var state: one RMState,
}

one sig TM {
	var state: one TMState
}

var sig TMPrepared in RM {}

pred TPInit {
	RM.state = RMWorking
	TM.state = TMInit
	no TMPrepared
	no Msgs
}

pred TMRcvPrepared[rm: RM] {
	TM.state = TMInit
	rm in Msgs

	TMPrepared' = TMPrepared + rm

	RM <: state' = RM <: state
	TM <: state' = TM <: state
	Msgs' = Msgs
}

pred TMCommit {
	TM.state = TMInit
	TMPrepared = RM

	TM.state' = TMCommitted
	Msgs' = Msgs + MsgCommit

	RM <: state' = RM <: state
	TMPrepared' = TMPrepared
}

pred TMAbort {
	TM.state = TMInit

	TM.state' = TMAborted
	Msgs' = Msgs + MsgAbort
	
	RM <: state' = RM <: state
	TMPrepared' = TMPrepared
}

pred RMPrepare[rm: RM] {
	rm.state = RMWorking

	RM <: state' = state ++ rm->RMPrepared
	 Msgs' = Msgs + rm

	TM.state' = TM.state
	TMPrepared' = TMPrepared
}

pred RMChooseToAbort[rm: RM] {
	rm.state = RMWorking

	RM <: state' = state ++ rm->RMAborted
	
	TM.state' = TM.state
	TMPrepared' = TMPrepared
	Msgs' = Msgs
}

pred RMRcvCommitMsg[rm: RM] {
	MsgCommit in Msgs

	RM <: state' = state ++ rm->RMCommitted

	TM.state' = TM.state
	TMPrepared' = TMPrepared
	Msgs' = Msgs
}

pred RMRcvAbortMsg[rm: RM] {
	MsgAbort in Msgs

	RM <: state' = state ++ rm->RMAborted
	
	TM.state' = TM.state
	TMPrepared' = TMPrepared
	Msgs' = Msgs
}

pred TPNext {
	TMCommit or TMAbort or some rm : RM {
		TMRcvPrepared[rm] or RMPrepare[rm] or RMChooseToAbort[rm] or
		RMRcvCommitMsg[rm] or RMRcvAbortMsg[rm]
	}
}


pred stuttering {
	TMPrepared' = TMPrepared
	RM <: state' = RM <: state
	TM <: state' = TM <: state
	Msgs' = Msgs

}

fact TPSpec {
	TPInit
	always (TPNext or stuttering)
}

run AllCommited {
	eventually RM.state = RMCommitted
} for exactly 3 RM, 11 steps 

run AllAborted {
	eventually RM.state = RMAborted
} for exactly 3 RM

assert TCConsistent {
	always {
		all rm1, rm2 : RM {
			not {
				rm1.state = RMAborted
				rm2.state = RMCommitted
			}
		}
	}
}
check TCConsistent for 1.. steps
