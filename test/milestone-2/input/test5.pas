program ArrayConstTest;
konstanta
    MAX_SIZE = 100;
    PI = 3.14159;
tipe
    IntArray = larik[1..10] dari integer;
    CharArray = larik[0..MAX_SIZE] dari char;
variabel
    numbers: IntArray;
    letters: CharArray;
    i: integer;
mulai
    untuk i := 1 ke 10 lakukan
        numbers[i] := i * 2;
    
    letters[0] := 'A';
    letters[1] := 'B';
    writeln('First number: ', numbers[1]);
    writeln('First letter: ', letters[0])
selesai.