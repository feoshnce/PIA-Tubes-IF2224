program NestedBlockTest;
var
  outer1, outer2: integer;
  flag: boolean;

procedure outer;
var
  inner1: integer;
  
  procedure nested;
  var
    deep: integer;
  begin
    deep := 5;
    outer1 := deep;
  end;
  
begin
  inner1 := 10;
  nested;
  outer2 := inner1;
end;

begin
  outer1 := 0;
  outer2 := 0;
  flag := false;
  
  while outer1 < 5 do
  begin
    outer1 := outer1 + 1;
    outer;
  end;
  
  if outer2 > 0 then
    flag := true;
end.