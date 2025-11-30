program Comprehensive;
tipe
    Student = rekaman
        id: integer;
        name: larik[1..50] dari char;
        gpa: real;
    selesai;
variabel
    students: larik[1..100] dari Student;
    count: integer;
    avg_gpa: real;

prosedur InitStudent(s: Student; student_id: integer);
mulai
    s.id := student_id;
    s.gpa := 0.0
selesai;

fungsi CalculateAverage(n: integer): real;
variabel
    i: integer;
    total: real;
mulai
    total := 0.0;
    i := 1;
    selama i <= n lakukan
    mulai
        total := total + students[i].gpa;
        i := i + 1
    selesai;
    CalculateAverage := total / n
selesai;

mulai
    count := 3;
    InitStudent(students[1], 1001);
    students[1].gpa := 3.5;
    InitStudent(students[2], 1002);
    students[2].gpa := 3.8;
    InitStudent(students[3], 1003);
    students[3].gpa := 3.2;
    avg_gpa := CalculateAverage(count)
selesai.
