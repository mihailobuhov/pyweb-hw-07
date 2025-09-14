--1-- Знайти 5 студентів із найбільшим середнім балом з усіх предметів
SELECT
    s.id AS student_id,
    s.fullname AS student_name,
    ROUND(AVG(g.grade), 2) AS average_grade
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.id
ORDER BY average_grade DESC
LIMIT 5;

--2-- Знайти студента із найвищим середнім балом з певного предмета
SELECT 
    s.id AS student_id, 
    s.fullname AS student_name, 
    ROUND(AVG(g.grade), 2) AS average_grade
FROM grades g
JOIN students s ON s.id = g.student_id
WHERE g.subject_id = 3  -- Предмет, з якого ви хочете знайти середній бал
GROUP BY s.id
ORDER BY average_grade DESC
LIMIT 1;

--3-- Знайти середній бал у групах з певного предмета
SELECT
    gr.name AS group_name,
    sb.name AS subject,
    ROUND(AVG(g.grade), 2) AS average_grade   
FROM groups gr
JOIN students s ON gr.id = s.group_id
JOIN grades g ON s.id = g.student_id
JOIN subjects sb ON g.subject_id = sb.id
WHERE g.subject_id = 3  -- Предмет, з якого ви хочете знайти середній бал
GROUP BY gr.name, sb.name
ORDER BY average_grade DESC;

--4-Знайти середній бал на потоці (по всій таблиці оцінок).
SELECT ROUND(AVG(grade), 2) AS average_grade
FROM grades;

--5-- Знайти які курси читає певний викладач.
SELECT 
    t.id AS teacher_id, 
    t.fullname AS teacher, 
    s.name AS subject
FROM teachers t
JOIN subjects s ON t.id = s.teacher_id
WHERE t.id = 3;

--6-- Знайти список студентів у певній групі.
SELECT 
	s.id AS student_id, 
	s.fullname AS student_name, 
	gr.name AS group_name
FROM groups gr 
JOIN students s ON gr.id = s.group_id 
WHERE gr.id = 3
ORDER BY s.id ASC;

--7-- Знайти оцінки студентів у окремій групі з певного предмета.
SELECT 
	s.id AS student_id, 
	s.fullname AS student_name, 
	gr.name AS group_name, 
	sb.name AS subject, 
	g.grade
FROM groups gr 
JOIN students s ON gr.id = s.group_id
JOIN grades g ON s.id = g.student_id
JOIN subjects sb ON sb.id = g.subject_id
WHERE g.subject_id = 5 AND s.group_id = 2
ORDER BY s.id ASC;

--8-- Знайти середній бал, який ставить певний викладач зі своїх предметів.
SELECT 
	t.fullname AS teacher,
	sb.name AS subject,
	ROUND(AVG(g.grade), 2) AS average_grade
FROM teachers t
JOIN subjects sb ON t.id = sb.teacher_id
JOIN grades g ON sb.id = g.subject_id
WHERE t.id = 2
GROUP BY t.fullname , sb.name
ORDER BY average_grade DESC;

--9-- Знайти список курсів, які відвідує студент.
SELECT DISTINCT
	s.id AS student_id,
    s.fullname AS student_name,
    sb.name AS subject
FROM grades g
JOIN students s ON s.id = g.student_id
JOIN subjects sb ON sb.id = g.subject_id 
WHERE s.id = 25
ORDER BY sb.name;

--10-- Знайти список курсів, які певному студенту читає певний викладач.
SELECT DISTINCT
	s.id AS student_id,
    s.fullname AS student_name,
    t.fullname AS teacher,
    sb.name AS subject    
FROM grades g
JOIN students s ON s.id = g.student_id
JOIN subjects sb ON sb.id = g.subject_id 
JOIN teachers t ON t.id = sb.teacher_id
WHERE s.id = 25 AND t.id = 2
ORDER BY sb.name;

--11-- Середній бал, який певний викладач ставить певному студентові.
SELECT 
	t.fullname AS teacher,
	s.fullname AS student,
	ROUND(AVG(g.grade), 2) AS average_grade
FROM teachers t
JOIN subjects sb ON t.id = sb.teacher_id
JOIN grades g ON sb.id = g.subject_id
JOIN students s ON s.id = g.student_id
WHERE t.id = 3 AND s.id = 15
GROUP BY t.fullname , s.fullname;
	
--12-- Оцінки студентів у певній групі з певного предмета на останньому занятті.
SELECT 
	s.id AS student_id , 
	s.fullname AS student, 
	gr.name AS groups, 
	sb.name AS subjects, 
	g.grade, 
	g.grade_date AS last_date
FROM grades g
JOIN students s ON g.student_id = s.id
JOIN subjects sb ON g.subject_id = sb.id
JOIN groups gr ON s.group_id = gr.id
WHERE g.subject_id = 2 AND s.group_id = 3 AND g.grade_date = (
	SELECT MAX(g.grade_date) AS last_date
	FROM grades g
	JOIN students s ON s.id = g.student_id 
	WHERE g.subject_id = 2 AND s.group_id = 3
);
