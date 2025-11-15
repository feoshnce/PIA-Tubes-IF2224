program ArrayStrictTest;
konstanta
    MAX_COUNT = 10;
variabel
    data_int: larik[1..MAX_COUNT] dari integer;
    i: integer;
    total: integer;
mulai
    total := 0;
    untuk i := 1 ke MAX_COUNT lakukan
    mulai
        data_int[i] := i * 2;
        total := total + data_int[i];
    selesai;
    writeln('Sum: ', total);
selesai.