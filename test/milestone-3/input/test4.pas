program NestedScope;
variabel
    global_x: integer;

prosedur Outer;
variabel
    outer_y: integer;

    prosedur Inner;
    variabel
        inner_z: integer;
    mulai
        inner_z := 1;
        outer_y := 2;
        global_x := 3
    selesai;

mulai
    outer_y := 10;
    Inner()
selesai;

mulai
    global_x := 100;
    Outer()
selesai.
