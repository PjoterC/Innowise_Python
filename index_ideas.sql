CREATE INDEX idx_students_room ON students(room);

DROP INDEX idx_students_room;

ANALYZE students;
SET enable_seqscan = on;
