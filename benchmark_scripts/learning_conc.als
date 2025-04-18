module learning_conc
open util/ordering[Process]

abstract sig PC {}
one sig a, b, Done extends PC {}

fun succ : Process -> Process {
	Process <: (next + last->first)
}

sig Process {
	var pc : one PC
}

var sig x, y in Process {}

pred Init {
	no x
	no y
	pc = Process->a
}

pred a[self:Process] {
	self.pc = a
	x' = x + self
	pc' = pc ++ self->b
	y' = y
}

pred b[self:Process] {
	self.pc = b
	succ.self in x implies y' = y + self else y' = y
	pc' = pc ++ self->Done
	x' = x
	
}

pred proc[self:Process] {
	a[self] or b[self]
}

pred Terminating {
	Process.pc = Done
	stuttering
}

pred stuttering {
	x' = x
	y' = y
	pc' = pc
}


pred Next {
	(some p: Process {proc[p]}) or Terminating
}

pred Fairness {
    always eventually Next
}

fact Spec {
	Init 
	always (Next or stuttering)
}

run {eventually Terminating} for exactly 5 Process, 1.. steps

pred PCorrect {
	always {
		// {(p1, a), (p2, b), (p3, Done)}
		//  Process = {p1, p2, p3}
		// Process.pc = {a, b, Done}
		// {a, b, Done} == {Done, Done Done}
		Process.pc = Done implies some y
	}
} 
check PCorrect { PCorrect } for 2 but 1.. steps
check PCorrect { PCorrect } for 2 but 1.. steps

pred Inv {
	always {
		all p : Process | (p.pc = b or p.pc = Done) implies (p in x)
		(some p : Process | p.pc != Done) or some y
	}
}
check Inv { Inv } for 2 but 1.. steps

assert Termination {
	Fairness implies eventually Process.pc = Done
} 
check Termination for 2 but 1.. steps

check {
	PCorrect and Inv
} for 2 but 1.. steps
