program ProcedureParams;
variabel
    x, y: integer;

prosedur Swap(var a, b: integer);
variabel
    temp: integer;
mulai
    temp := a;
    a := b;
    b := temp
selesai;

mulai
    x := 10;
    y := 20;
    Swap(x, y)
selesai.
