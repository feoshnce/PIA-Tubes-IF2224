program NestedCompoundTest;
variabel
    x, y: integer;
    done: boolean;
mulai
    x := 0;
    done := false; 
    selama tidak done lakukan 
    mulai
        x := x + 1;
        y := x * 2;
        
        jika y > 5 maka
            mulai
                writeln(y);
                done := true
            selesai
        selain-itu
            done := false;
    selesai; 

    mulai
        mulai
            x := x + 1
        selesai
    selesai
selesai.