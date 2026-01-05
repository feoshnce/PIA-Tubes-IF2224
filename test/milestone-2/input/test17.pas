program DeepNesting;
variabel
    i, j, total: integer;
    ok: boolean;

mulai
    total := 0;
    i := 1;

    selama i <= 3 lakukan
    mulai
        j := 1;
        selama j <= 3 lakukan
        mulai
            jika (i + j) mod 2 = 0 maka
            mulai
                total := total + (i * j) + (i + j) * (i - j)
            selesai
            selain-itu
            mulai
                total := total + (i * j) - (i + j)
            selesai;
            j := j + 1
        selesai;
        i := i + 1
    selesai;

    ok := total >= 0;
    jika ok maka
        writeln(total)
    selain-itu
        writeln(0)
selesai.
