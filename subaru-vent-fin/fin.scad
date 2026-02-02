$fn = 90;

EPS = 0.001;

WIDTH = 92.0;
HEIGHT = 14.8;
DEPTH = 2.4;

OVERHANG_W = (92.9 -WIDTH)/2;
OVERHANG_H = 3.2;

ANCHOR_PIN_L = 2.0;

CLICK_PIN_D = 1.7;
CLICK_PIN_L = 1.9;

RECESS_W = WIDTH - 90.6;
RECESS_OFFSET = 9.2;
M = 10;

DRIVING_PIN_D = 1.5;
DRIVING_PIN_L = 2.0;
DRIVING_PIN_HEAD_D = 2;


module edge(o1=0, o2=0) {
    translate([-o1, 0, DEPTH/2])
        rotate([0,90,0])
            cylinder(d=DEPTH, h=WIDTH + o1 + o2);
}

module click_pin() {
    translate([-OVERHANG_W, 0, DEPTH/2])
        rotate([0,90,0])
            cylinder(d=CLICK_PIN_D, h=2*CLICK_PIN_L, center=true);
}

module overhang() {
    translate([-OVERHANG_W, 0,0])
        cube([WIDTH + 2*OVERHANG_W, OVERHANG_H, DEPTH]);    
}

module body() {
    HEIGHT_REDUCED = HEIGHT - DEPTH;
    cube([WIDTH, HEIGHT_REDUCED, DEPTH]);    
    overhang();

    edge(o2 = OVERHANG_W + ANCHOR_PIN_L, o1 = OVERHANG_W);
    translate([0,HEIGHT_REDUCED,0])
        edge();
}

module recess() {
    translate([WIDTH - RECESS_W, RECESS_OFFSET - DEPTH/2, -M/2])
        cube([M, M, M]);
}

module driving_pin() {
    translate([
        WIDTH - RECESS_W-DRIVING_PIN_L,
        HEIGHT - DEPTH,
        DRIVING_PIN_D/2
    ]) {
        rotate([0,90,0])
            cylinder(d=DRIVING_PIN_D, h=2*DRIVING_PIN_L);
    }
    translate([
        WIDTH - RECESS_W+DRIVING_PIN_L-EPS,
        HEIGHT - DEPTH,
        DRIVING_PIN_HEAD_D/2
    ]) {
        rotate([0,90,0])
            cylinder(d1=DRIVING_PIN_HEAD_D, d2=DRIVING_PIN_D, h=1);
    }
}

module fin() {
    difference() {
        body();
        recess();
    }
    driving_pin();
    click_pin();
}

fin();