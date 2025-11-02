program ConditionalTest;
var
    score: integer;
    grade: char;
begin
    score := 85;
    if score >= 80 then
        grade := 'A'
    else
        if score >= 70 then
            grade := 'B'
        else
            grade := 'C'
end.