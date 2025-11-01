program TestLarik;
variabel
  angka: larik[1..10] dari integer;
  i, j, total: integer;
mulai
  total := 0;
  untuk i := 1 ke 10 lakukan
  mulai
    angka[i] := i * 2;
    total := total + angka[i]
  selesai;
  untuk j := 10 turun-ke 1 lakukan
    writeln(angka[j])
selesai.
