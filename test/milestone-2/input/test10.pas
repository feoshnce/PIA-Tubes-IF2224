program ComplexDeclarationsTest;
konstanta
    A = 1;
    B = 2;
    C = 3;
tipe
    Range1 = 1..100;
    Range2 = 'a'..'z';
    Vector = larik[1..5] dari integer;
variabel
    r1: Range1;
    r2: Range2;
    v: Vector;

prosedur MultiParam(x: integer; y: real; z: char; flag: boolean);
mulai
    writeln(x)
selesai;

fungsi ChainedFunc(a: integer): integer;
variabel
    local: integer;
mulai
    local := a;
    ChainedFunc := local
selesai;

mulai
    r1 := 50;
    r2 := 'm';
    v[1] := 10;
    
    MultiParam(100, 3.14, 'X', true);
    
    r1 := ChainedFunc(ChainedFunc(5));
    
    jika tidak ((r1 = 5) atau (r1 <> 10)) dan (r2 >= 'a') maka
        mulai
        selesai
    selain-itu
        mulai
        selesai
selesai.