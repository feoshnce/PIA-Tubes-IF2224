program StringCharTest;
var
  name: char;
  message: array[1..5] of char;
{ This is a comment with special chars: :=, <>, >= }
const
  greeting = 'Hello, World!';
  symbol = '+';
begin
  name := 'A';
  (* Multi-line comment
     with div and mod operators *)
  writeln('Name: ', name);
  writeln('Special chars: {}()[]');
end.