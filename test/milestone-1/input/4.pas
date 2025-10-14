program ProcFuncTest;
type
  MyRange = 1..100;
var
  a, b: MyRange;
  
procedure swap(x, y: integer);
var
  temp: integer;
begin
  temp := x;
  x := y;
  y := temp;
end;

function calculate(m, n: integer): integer;
begin
  calculate := m div n + m mod n;
end;

begin
  a := 50;
  b := calculate(100, 7);
  swap(a, b);
end.