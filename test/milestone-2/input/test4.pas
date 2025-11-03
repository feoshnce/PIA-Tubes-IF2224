program ProcFuncTest;
variabel
    x, y, result: integer;

prosedur PrintSum(a, b: integer);
variabel
    total: integer;
mulai
    total := a + b;
    writeln('Sum is: ', total)
selesai;

fungsi Multiply(m, n: integer): integer;
mulai
    Multiply := m * n
selesai;

mulai
    x := 5;
    y := 3;
    PrintSum(x, y);
    result := Multiply(x, y);
    writeln('Product is: ', result)
selesai.