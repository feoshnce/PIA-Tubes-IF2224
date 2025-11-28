program ComplexExpressions;
variabel
    a, b, c: integer;
    x, y: real;
    flag: boolean;
mulai
    a := 10;
    b := 20;
    c := 30;
    x := (a + b) * c;
    y := x / 2.0;
    flag := (a < b) and (b < c);
    flag := not flag or (a = 10)
selesai.
