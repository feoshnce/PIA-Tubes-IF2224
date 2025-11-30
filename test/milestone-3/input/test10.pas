program ControlFlow;
variabel
    x, y, max: integer;
    i, sum: integer;
mulai
    x := 10;
    y := 20;
    
    jika x > y maka
        max := x
    selain-itu
        max := y;

    sum := 0;
    i := 1;
    selama i <= 10 lakukan
    mulai
        sum := sum + i;
        i := i + 1
    selesai
selesai.
