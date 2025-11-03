program ComplexDeclarationsTest;
const
    A = 1;
    B = 2;
    C = 3;
type
    Range1 = 1..100;
    Range2 = 'a'..'z';
    Matrix = array[1..5] of array[1..5] of integer;
var
    r1: Range1;
    r2: Range2;
    m: Matrix;

procedure MultiParam(x: integer; y: real; z: char; flag: boolean);
begin
    writeln(x)
end;

function ChainedFunc(a: integer): integer;
var
    local: integer;
begin
    local := a;
    ChainedFunc := local
end;

begin
    r1 := 50;
    r2 := 'm';
    m[1][1] := 10;
    
    MultiParam(100, 3.14, 'X', true);
    
    r1 := ChainedFunc(ChainedFunc(5));
    
    if not ((r1 = 5) or (r1 <> 10)) and (r2 >= 'a') then
        begin
        end
    else
        begin
        end
end.