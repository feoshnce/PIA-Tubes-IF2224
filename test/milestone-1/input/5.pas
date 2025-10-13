program NumberEdgeCase;
var
  integer1, real1: real;
  variable, vari, var123: integer;
  beginend, ifelse: boolean;
begin
  integer1 := 42;
  real1 := 3.14159;
  variable := 0;
  var123 := -999;
  
  if integer1 >= real1 then
    beginend := true;
    
  vari := integer1 + real1 * 2 - 1;
  ifelse := (vari <> 0) and (var123 <= -100);
end.