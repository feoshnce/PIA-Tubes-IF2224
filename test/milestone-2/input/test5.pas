program ArrayConstTest;
const
    MAX_SIZE = 100;
    PI = 3.14159;
type
    IntArray = array[1..10] of integer;
    CharArray = array[0..MAX_SIZE] of char;
var
    numbers: IntArray;
    letters: CharArray;
    i: integer;
begin
    for i := 1 to 10 do
        numbers[i] := i * 2;
    
    letters[0] := 'A';
    letters[1] := 'B';
    writeln('First number: ', numbers[1]);
    writeln('First letter: ', letters[0])
end.