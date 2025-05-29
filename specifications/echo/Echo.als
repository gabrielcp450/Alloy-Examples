module Echo
/***************************** Alloy vs TLA+ **********************************)
(* This file is part of a project to rewrite TLA+ examples into Alloy,        *)
(* preserving structure and intent while exploring their differences.         *)
(*                                                                            *)
(* ORIGINAL HEADER:                                                           *)
(* The Echo algorithm for constructing a spanning tree in an undirected       *)
(* graph starting from a single initiator, as a PlusCal algorithm.            *)
(*                                                                            *)
(******************************************************************************/

enum PC {n0, n1, n2, Done}

// In Alloy, sigs abstract over possible instances while ensuring structural 
// constraints.  In contrast, CONSTANTs in TLA+ lock the model to a particular 
// shape or domain.
abstract sig Type {}

one sig Explorer, Echo extends Type {}

sig Node {
	neighbors : set Node,
	var pc : one PC,
	var parent : lone Node,
	var children : set Node,
	var rcvd : set Node,
	var inbox : Type -> Node
}
one sig Initiator in Node {}

// Keyword 'fact' declares global constraints that always hold, it's equivalent
// to ASSUME.
fact Assumptions {
  // No edge from a node to itself (self-loops).
  no neighbors & iden

  // Undirected graph (there exists an edge from b 
  // to a if there exists an edge from a to b).
  neighbors = ~neighbors

  // There exists a spanning tree consisting of *all* nodes.
  // (no forest of spanning trees). 
  all n: Node | Node in n.*neighbors
}

pred Init {
	no inbox
	no parent
	no children
	no rcvd
	pc = Node->n0
}

pred n0[n : Node] {
	n.pc = n0
	(n = Initiator) implies {
		inbox' = inbox + n.neighbors->Explorer->n
	} else {
		inbox' = inbox
	}
	pc' = pc ++ n->n1
	parent' = parent
	children' = children
	rcvd' = rcvd
}

pred n1[n : Node] {
	n.pc = n1
	(n.rcvd = n.neighbors) implies {
		pc' = pc ++ n->n2
		inbox' = inbox
		parent' = parent	
		children' = children
		rcvd' = rcvd
	} else {
		some p : Node, t : Type {
			t->p in n.inbox
			rcvd' = rcvd + n->p
			n != Initiator and no n.rcvd implies {
				inbox' = inbox - n->t->p + (n.neighbors-p)->Explorer->n
				parent' = parent + n->p
			} else {
				inbox' = inbox - n->t->p
				parent' = parent
			}
			t = Echo implies {
				children' = children + n->p
			} else {
				children' = children
			}
		}
		pc' = pc
	}
}

pred n2[n : Node] {
	n.pc = n2
	n != Initiator implies {
		inbox' = inbox + n.parent->Echo->n
	} else {
		inbox' = inbox
	}
	pc' = pc ++ n->Done
	children' = children
	rcvd' = rcvd
	parent' = parent	
}

pred node[n: Node] {
	n0[n] or n1[n] or n2[n]
}

pred stuttering {
 	pc' = pc
	children' = children
	parent' = parent
	rcvd' = rcvd
	inbox' = inbox
}

pred Terminating {
	Node.pc = Done
	stuttering
}

pred Next {
	(some n : Node | node[n]) or Terminating
}

// Keyword 'fact' declares global constraints that always hold, it's also
// equivalent to SPECIFICATION inside the config file.
fact Spec {
	Init 
	always (Next or stuttering)
}

run Example {
	all n : Node | n.neighbors = Node-n
	eventually Node.pc = Done
} for exactly 3 Node, 1..20 steps

// There's no need for checking types since Alloy is a strongly typed language.
pred TypeOK {}

check InitiatorNoParent {
	always {
		no Initiator.parent
	}
}

check ParentIsNeighbor {
	always {
		parent in neighbors 
	}
}

check ParentChild {
	always {
		children in ~parent
		parent :> pc.Done in ~children
	}
}

check AncestorProperties {
	always {
		Node.pc = Done implies (Node-Initiator = ^parent.Initiator) and (no ^parent & iden)
	}
} for 3 but 1..steps
