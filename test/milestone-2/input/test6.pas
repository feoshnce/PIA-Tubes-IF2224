program ComplexExpressionTest;
variabel
    a, b, c: integer;
    x, y: real;
    flag, result: boolean;
mulai
    a := 10;
    b := 5;
    c := 3;
    
    x := (a + b) * c / 2.0;
    y := a bagi b + c mod 2;
    
    flag := (a > b) dan (b < c);
    result := tidak flag atau (a <> c);
    
    jika (a >= 10) dan ((b <= 5) atau (c = 3)) maka
        writeln('Condition is true')
    selain-itu
        writeln('Condition is false')
selesai.