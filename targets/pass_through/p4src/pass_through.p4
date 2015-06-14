// Include headers and parser information.
#include "includes/headers.p4"
#include "includes/parser.p4"


// Create actions to be used in the tables.
action set_egr(egress_spec) {
    modify_field(standard_metadata.egress_spec, egress_spec);
}

action _no_op() {
}

action _drop() {
    drop();
}


// Create tables.
table forward {
    reads {
        ethernet.dstAddr : exact;
    }
    actions {
        _drop;
        set_egr;
    }
    size : 2;
}

table pass_through {
    reads {
        ethernet.dstAddr : exact;
    }
    actions {
        _no_op;
    }
    size : 2;
}


// Control flow for how the tables will be processed.
control ingress {
    apply(forward);
}

control egress {
    apply(pass_through);
}
