program LogicalTest;
var
  x, y, z: integer;
  result: boolean;
begin
  x := 10;
  y := 20;
  z := 15;
  if (x < y) and (z >= x) then
    result := true
  else if (x > y) or (x <> z) then
    result := false
  else if not (x <= z) then
    result := true;
end.