program EmptyDowntoTest;
var
    i: integer;

procedure EmptyProc;
begin
end;

function EmptyFunc: integer;
begin
    EmptyFunc := 0
end;

begin
    for i := 10 downto 1 do
        EmptyProc;
    
    i := EmptyFunc()
end.