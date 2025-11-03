program NestedCompoundTest;
var
    x, y: integer;
    done: boolean;
begin
    x := 0;
    repeat
        x := x + 1;
        begin
            y := x * 2;
            if y > 5 then
                begin
                    writeln(y);
                    done := true
                end
            else
                done := false
        end
    until done;
    
    begin
        begin
            x := x + 1
        end
    end
end.