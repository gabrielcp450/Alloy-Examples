abstract sig Process {}

one sig p, c extends Process {}

var sig on in Process {}

pred Init {
	no on
}

pred ProducerStep {
	(on = p + c) implies (
		on' = c
	)

	(no on) implies (
		on' = p
	)
}

pred ConsumerStep {
	(on = p) implies (
		on' = p + c
	)
	(on = c) implies (
		no on'
	)
}

pred Next {
	ProducerStep or ConsumerStep
}

pred Fairness {
    always eventually Next
}

pred stuttering {
	on' = on
}

fact Spec {
	Init
	always (Next or stuttering)
	Fairness
}

run {} for exactly 12 steps
