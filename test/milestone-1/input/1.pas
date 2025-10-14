program ArrayTest;
var
  numbers: array[1..10] of integer;
  i, j, sum: integer;
begin
  sum := 0;
  for i := 1 to 10 do
  begin
    numbers[i] := i * 2;
    sum := sum + numbers[i];
  end;
  for j := 10 downto 1 do
    writeln(numbers[j]);
end.