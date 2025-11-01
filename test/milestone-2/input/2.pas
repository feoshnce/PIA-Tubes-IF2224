program TestKomprehensif;
variabel
  angka: larik[1..5] dari integer;
  i, x, y: integer;
  hasil: boolean;
mulai
  x := 10;
  y := 5;

  { Test if-then-else dengan selain-itu }
  jika x > y maka
    hasil := true
  selain-itu
    hasil := false;

  { Test for dengan ke }
  untuk i := 1 ke 5 lakukan
    angka[i] := i;

  { Test for dengan turun-ke }
  untuk i := 5 turun-ke 1 lakukan
    writeln(angka[i])
selesai.
