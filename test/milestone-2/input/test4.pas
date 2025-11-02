program ProcFuncTest;
var
    x, y, result: integer;

procedure PrintSum(a, b: integer);
var
    total: integer;
begin
    total := a + b;
    writeln('Sum is: ', total)
end;

function Multiply(m, n: integer): integer;
begin
    Multiply := m * n
end;

begin
    x := 5;
    y := 3;
    PrintSum(x, y);
    result := Multiply(x, y);
    writeln('Product is: ', result)
end.