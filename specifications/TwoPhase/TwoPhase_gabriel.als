abstract sig State {}

one sig on, off extends State {}

abstract sig Process {
    var state: one State
}

fun succ :  State -> State {
    (off -> on + on -> off)
}

one sig p, c extends Process {}

pred Init {
    p.state = off
    c.state = off
    
}

pred ProducerStep {
	p.state = c.state
 	p.state' = (p.state).succ
	c.state' = c.state
}

pred ConsumerStep {
	p.state != c.state
	c.state' = (c.state).succ
	p.state' = p.state
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
