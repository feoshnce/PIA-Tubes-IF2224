program LoopTest;
var
    i, sum, count: integer;
begin
    sum := 0;
    for i := 1 to 10 do
        sum := sum + i;
    
    count := 0;
    while count < 5 do
        count := count + 1
end.