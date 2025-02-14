# SQL Commands Documentation

## Task2-1: Create and Use Database
```sql
CREATE DATABASE website;
USE website;
```

## Task2-2: Create Member Table
```sql
CREATE TABLE member(
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    follower_count INT UNSIGNED NOT NULL DEFAULT 0,
    time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

## Task3-1: Insert Data into Member Table
```sql
INSERT INTO member (name, username, password) VALUES ('test', 'test', 'test');
INSERT INTO member (name, username, password, follower_count) VALUES
    ('Alice', 'alice1', 'password1', 1),
    ('Bob', 'bob2', 'password2', 2),
    ('Charlie', 'charlie3', 'password3', 3),
    ('David', 'david4', 'password4', 4);
```

## Task3-2: Select All Members
```sql
SELECT * FROM member;
```

## Task3-3: Select All Members Ordered by Time Descending
```sql
SELECT * FROM member ORDER BY time DESC;
```

## Task3-4: Select Members Ordered by Time Descending with Limit and Offset
```sql
SELECT * FROM member ORDER BY time DESC LIMIT 3 OFFSET 1;
```

## Task3-5: Select Member by Username
```sql
SELECT * FROM member WHERE username="test";
```

## Task3-6: Select Members with Name Containing 'es'
```sql
SELECT * FROM member WHERE name LIKE '%es%';
```

## Task3-7: Select Member by Username and Password
```sql
SELECT * FROM member WHERE username="test" AND password="test";
```

## Task3-8: Update Member Name
```sql
SET SQL_SAFE_UPDATES=0;
UPDATE member SET name="test2" WHERE username="test";
```

## Task4-1: Count Total Members
```sql
SELECT COUNT(id) FROM member;
```

## Task4-2: Sum of Follower Counts
```sql
SELECT SUM(follower_count) FROM member;
```

## Task4-3: Average Follower Count
```sql
SELECT AVG(follower_count) FROM member;
```

## Task4-4: Average Follower Count of Top 2 Members
```sql
SELECT AVG(follower_count) FROM (
    SELECT follower_count FROM member ORDER BY follower_count DESC LIMIT 2
) AS top_followers;
```

## Task5-1: Create Message Table and Insert Data
```sql
CREATE TABLE message(
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    member_id BIGINT NOT NULL,
    content VARCHAR(255) NOT NULL,
    like_count INT UNSIGNED NOT NULL DEFAULT 0,
    time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE message ADD FOREIGN KEY (member_id) REFERENCES member(id);

INSERT INTO message(member_id, content, like_count) VALUES
    (1, "content1", 1),
    (1, "content11", 11),
    (1, "content111", 111),
    (2, "content2", 2),
    (2, "content22", 22),
    (2, "content222", 222),
    (3, "content3", 3),
    (3, "content33", 33),
    (3, "content333", 333),
    (4, "content4", 4),
    (4, "content44", 44),
    (4, "content444", 444),
    (5, "content5", 5),
    (5, "content55", 55),
    (5, "content555", 555);
```

## Task5-2: Join Member and Message Tables
```sql
SELECT * FROM member INNER JOIN message ON member.id = message.member_id;
```

## Task5-3: Join Member and Message Tables for a Specific User
```sql
SELECT * FROM member INNER JOIN message ON member.id = message.member_id WHERE member.username="test";
```

## Task5-4: Calculate Average Like Count for User 'test'
```sql
SELECT AVG(message.like_count) AS avg_like_count
FROM member INNER JOIN message ON member.id = message.member_id
WHERE member.username="test";
```

## Task5-5: Calculate Average Like Count for Each User
```sql
SELECT AVG(like_count) AS avg_like_count
FROM member INNER JOIN message ON member.id = message.member_id
GROUP BY member.username;
```

