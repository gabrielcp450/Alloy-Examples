abstract sig Type {}

one sig Req, Ack, Rel in Type {}

sig Proc {
    var ack: set Proc,
    var network: Proc -> (seq Type)
}

var sig crit in Proc {}

pred Init {
    no ack
    no network
    no crit
}

pred beats[p: Proc, q: Proc] {
    
}

pred Broadcast[s: Proc, m: Type] {
    all r : Proc {
        (s = r) implies (
            r.(s.network') = r.(s.network)
        ) else (
            r.(s.network') = r.(s.network).add[m]
        )
    }
}

pred Request[p: Proc] {
    (Proc - p).network' = (Proc - p).network
    Broadcast[p, Req]
    ack' = ack ++ (p -> p)
    crit' = crit
}

pred ReceiveRequest[p: Proc, q: Proc] {
    some p.(q.network)
    let m = (p.(q.network)).first {
        m = Req
        network' = network ++ (q -> p -> p.(q.network).delete[0]) ++
                              (p -> q -> q.(p.network).add[Ack])
        ack' = ack
        crit' = crit
    }
}

pred ReceiveAck[p:Proc, q:Proc] {
	some p.(q.network)
	let m = (p.(q.network)).first {
		m = Ack
		no p.ack'
		(Proc - p).ack' = (Proc - p).ack
		network' = network ++ (q -> p -> p.(q.network).delete[0]) 
		//clock'  = clock
		//req' = req
		crit' = crit
	}
}

pred Enter[p:Proc] {
	 p.ack = Proc
	all q : (Proc - p)  | beats[p,q]
	crit' = crit + p
	// clock' = clock
	//req' = req
	ack' = ack
	network' = network
}	

pred Exit[p:Proc] {
	p in crit
	crit' = crit  - p
	Broadcast[p, Rel]
	//req' = 
	no p.ack'
	(Proc - p).ack' = (Proc - p).ack
	// clock' = clock	

}

pred ReceiveRelease[p:Proc, q:Proc] {
	some  p.(q.network)
	let m = (p.(q.network)).first {
		m = Rel
		// req
		network'  = network ++ (q -> p -> p.(q.network).delete[0]) 
		// clock' = clock
		ack' = ack
		crit' = crit
	}
}
		

pred Next {
	some p : Proc { 
		Request[p] or Enter[p] or Exit[p]
	}
	some p: Proc {
		some q : Proc - p |
			ReceiveRequest[p,q] or ReceiveAck[p,q] or ReceiveRelease[p,q]
	}
}


pred stuttering {
    ack' = ack
    network' = network
    crit' = crit
}

pred Fairness {
    always eventually Next
}

pred Spec {
    Init
    always Next or stuttering
    Fairness
}

pred BoundedNetwork {
	#(Proc.(Proc.network)) <=3
}

pred Mutex {
	lone crit
}

run {
    Spec
}