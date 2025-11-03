program NestedCompoundTest;
variabel
    x, y: integer;
    done: boolean;
mulai
    x := 0;
    ulangi
        x := x + 1;
        mulai
            y := x * 2;
            jika y > 5 maka
                mulai
                    writeln(y);
                    done := true
                selesai
            selain-itu
                done := false
        selesai
    sampai done;
    
    mulai
        mulai
            x := x + 1
        selesai
    selesai
selesai.