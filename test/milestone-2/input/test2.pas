program ConditionalTest;
variabel
    score: integer;
    grade: char;
mulai
    score := 85;
    jika score >= 80 maka
        grade := 'A'
    selain-itu
        jika score >= 70 maka
            grade := 'B'
        selain-itu
            grade := 'C'
selesai.