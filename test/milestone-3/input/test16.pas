program NestedBlocksExpressions;
variabel
    arr: larik[1..3] dari integer;
    i: integer;

fungsi AddMul(x: integer; y: integer): integer;
mulai
    AddMul := (x + y) * (x - y)
selesai;

prosedur FillAndPrint();
variabel
    j: integer;
mulai
    untuk j := 1 ke 3 lakukan
    mulai
        arr[j] := AddMul(j, j + 1);
        jika arr[j] > 0 maka
            writeln(arr[j])
        selain-itu
            writeln(0)
    selesai
selesai;

mulai
    FillAndPrint()
selesai.
