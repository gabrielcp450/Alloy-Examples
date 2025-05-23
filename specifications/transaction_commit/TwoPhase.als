abstract sig RMState {}
abstract sig TMState {}
abstract sig MsgType {}

one sig RMWorking, RMPrepared, RMCommitted, RMAborted extends RMState {}
one sig TMInit, TMCommitted, TMAborted extends TMState {}
one sig MsgPrepared, MsgCommit, MsgAbort extends MsgType {}

sig RM {
	var state: one RMState,
	var msgs: set MsgType
}

one sig TM {
	var state: one TMState
}

var sig TMPrepared in RM {}

pred TPInit {
	RM.state = RMWorking
	TM.state = TMInit
	no TMPrepared
	no RM.msgs
}

pred TMRcvPrepared[rm: RM] {
	TM.state = TMInit
	MsgPrepared in rm.msgs
	TMPrepared' = TMPrepared + rm

	all rm2 : RM | rm2.state' = rm2.state
	all tm2 : TM | tm2.state' = tm2.state
	all rm2 : RM | rm2.msgs' = rm2.msgs
}

pred TMCommit {
	TM.state = TMInit
	TMPrepared = RM
	TM.state' = TMCommitted
	all rm : RM | rm.msgs' = rm.msgs + MsgCommit

	all rm2 : RM | rm2.state' = rm2.state
	TMPrepared' = TMPrepared
}

pred TMAbort {
	TM.state = TMInit
	TM.state' = TMAborted
	all rm : RM | rm.msgs' = rm.msgs + MsgAbort
	
	all rm2 : RM | rm2.state' = rm2.state
	TMPrepared' = TMPrepared
}

pred RMPrepare[rm: RM] {
	rm.state = RMWorking
	rm.state' = RMPrepared
	all rm2 : RM - rm | rm2.state' = rm2.state
	rm.msgs' = rm.msgs + MsgPrepared
	all rm2: RM - rm | rm2.msgs' = rm2.msgs

	all tm2 : TM | tm2.state' = tm2.state
	TMPrepared' = TMPrepared
}

pred RMChooseToAbort[rm: RM] {
	rm.state = RMWorking
	rm.state' = RMAborted
	all rm2 : RM - rm | rm2.state' = rm2.state
	
	all tm2 : TM | tm2.state' = tm2.state
	TMPrepared' = TMPrepared
	all rm2 : RM | rm2.msgs' = rm2.msgs
}

pred RMRcvCommitMsg[rm: RM] {
	MsgCommit in rm.msgs
	rm.state' = RMCommitted
	all rm2 : RM - rm | rm2.state' = rm2.state

	all tm2 : TM | tm2.state' = tm2.state
	TMPrepared' = TMPrepared
	all rm2 : RM | rm2.msgs' = rm2.msgs
}

pred RMRcvAbortMsg[rm: RM] {
	MsgAbort in rm.msgs
	rm.state' = RMAborted
	all rm2 : RM - rm | rm2.state' = rm2.state

	all tm2 : TM | tm2.state' = tm2.state
	TMPrepared' = TMPrepared
	all rm2 : RM | rm2.msgs' = rm2.msgs
}

pred TPNext {
	TMCommit or TMAbort or some rm : RM {
		TMRcvPrepared[rm] or RMPrepare[rm] or RMChooseToAbort[rm] or
		RMRcvCommitMsg[rm] or RMRcvAbortMsg[rm]
	}
}

pred Fairness {
	always eventually TPNext
}

pred stuttering {
	all rm : RM { 
		rm.state' = rm.state
		rm.msgs' = rm.msgs
	}
	all tm : TM | tm.state' = tm.state
	TMPrepared' = TMPrepared

}

fact TPSpec {
	TPInit
	always (TPNext or stuttering)
	Fairness
}

fact {
	#RM = 3
}

