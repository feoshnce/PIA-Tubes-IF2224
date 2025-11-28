program ControlFlow;
variabel
    x, y, max: integer;
    i, sum: integer;
mulai
    x := 10;
    y := 20;
    
    if x > y then
        max := x
    else
        max := y;
    
    sum := 0;
    i := 1;
    while i <= 10 do
    mulai
        sum := sum + i;
        i := i + 1
    selesai
selesai.
