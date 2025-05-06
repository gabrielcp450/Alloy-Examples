---------- MODULE MCEcho ----------
EXTENDS Echo

N1 == {"a", "b", "c", "d"}

I1 == "d"

R1 == (
<<"a", "a">> :> FALSE @@
<<"a", "b">> :> TRUE @@
<<"a", "c">> :> TRUE @@
<<"a", "d">> :> TRUE @@
<<"b", "a">> :> TRUE @@
<<"b", "b">> :> FALSE @@
<<"b", "c">> :> TRUE @@
<<"b", "d">> :> TRUE @@
<<"c", "a">> :> TRUE @@
<<"c", "b">> :> TRUE @@
<<"c", "c">> :> FALSE @@
<<"c", "d">> :> TRUE @@
<<"d", "a">> :> TRUE @@
<<"d", "b">> :> TRUE @@
<<"d", "c">> :> TRUE @@
<<"d", "d">> :> FALSE
)

\* Print R and initiator to stdout at startup.
TestSpec == PrintT(R) /\ PrintT(initiator) /\ Spec        
===================================
