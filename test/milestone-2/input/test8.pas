program EmptyDowntoTest;
variabel
    i: integer;

prosedur EmptyProc;
mulai
selesai;

fungsi EmptyFunc: integer;
mulai
    EmptyFunc := 0
selesai;

mulai
    untuk i := 10 turun-ke 1 lakukan
        EmptyProc();
    
    i := EmptyFunc()
selesai.