program ComplexExpressionTest;
var
    a, b, c: integer;
    x, y: real;
    flag, result: boolean;
begin
    a := 10;
    b := 5;
    c := 3;
    
    x := (a + b) * c / 2.0;
    y := a div b + c mod 2;
    
    flag := (a > b) and (b < c);
    result := not flag or (a <> c);
    
    if (a >= 10) and ((b <= 5) or (c = 3)) then
        writeln('Condition is true')
    else
        writeln('Condition is false')
end.