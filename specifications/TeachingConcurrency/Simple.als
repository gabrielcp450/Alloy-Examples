module Simple
/***************************** Alloy vs TLA+ **********************************)
(* This file is part of a project to rewrite TLA+ examples into Alloy,        *)
(* preserving structure and intent while exploring their differences.         *)
(*                                                                            *)
(* ORIGINAL HEADER:                                                           *)
(* This is a trivial example from the document "Teaching Conccurrency"        *)
(* that appeared in                                                           *)
(*                                                                            *)
(*     ACM SIGACT News Volume 40, Issue 1 (March 2009), 58–62                 *)
(*                                                                            *)
(* A copy of that article is at                                               *)
(*                                                                            *)
(*    http://lamport.azurewebsites.net/pubs/teaching-concurrency.pdf          *)
(*                                                                            *)
(* It is also the example in Section 7.2 of "Proving Safety Properties",      *)
(* which is at                                                                *)
(*                                                                            *)
(*    http://lamport.azurewebsites.net/tla/proving-safety.pdf                 *)
(*                                                                            *)
(******************************************************************************/

open util/ordering[Process]

// In Alloy, sigs abstract over possible instances while ensuring structural 
// constraints.  In contrast, CONSTANTs in TLA+ lock the model to a particular 
// shape or domain.
abstract sig PC {}

one sig a, b, Done extends PC {}

sig Process {
	var pc : one PC
}

var sig x, y in Process {}

// This function defines successor relation in Processes, it’s similar to 
// writing x[(i - 1) % N] in TLA+, where you manually compute the successor with
// modular arithmetic.
fun succ : Process -> Process {
	Process <: (next + last->first)
}

pred Init {
	no x
	no y
	pc = Process->a
}

pred a[self: Process] {
	self.pc = a
	x' = x + self
	pc' = pc ++ self->b
	y' = y
}

pred b[self: Process] {
	self.pc = b
	succ.self in x implies y' = y + self else y' = y
	pc' = pc ++ self->Done
	x' = x
}

pred proc[self: Process] {
	a[self] or b[self]
}

pred stuttering {
	x' = x
	y' = y
	pc' = pc
}

pred Terminating {
	Process.pc = Done
	stuttering
}

pred Next {
	(some p : Process | proc[p]) or Terminating
}

// Keyword 'fact' declares global constraints that always hold, it's equivalent
// to SPECIFICATION inside the config file.
fact Spec {
	Init 
	always (Next or stuttering)
}

// In order to check Termination of this system, fairness is required because 
// without it, infinite stuttering sequences would be legal but prevent progress
// to Done.
pred Fairness {
    always eventually Next
}

check Termination {
	Fairness implies eventually Process.pc = Done
} for 3 but 1..steps

pred PCorrect {
	always {
		Process.pc = Done implies some y
	}
} 

// There's no need for checking types since Alloy is a strongly typed language.
pred TypeOK {}

pred Inv {
	always {
		all p : Process | (p.pc = b or p.pc = Done) implies (p in x)
		(some p : Process | p.pc != Done) or some y
	}
}

check Invariants {
	PCorrect and Inv
} for 3 but 1..steps
