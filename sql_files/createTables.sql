/*
    Abdulaziz Faraj, 2152135999
    Abdullah Alosaimi, 2172131914
    Mohamad Selman, 2181156265

    CS470_Project_CSHUB
*/

CREATE TABLE DEPARTMENT
(
    dept_id INT(4),
    dept_name VARCHAR(25) NOT NULL,

    CONSTRAINT dept_deptid_PK PRIMARY KEY (dept_id),
    CONSTRAINT dept_deptname_UK UNIQUE (dept_name)
);


CREATE TABLE COURSE
(
    dept_id INT(4),
    course_id INT(7),
    course_name VARCHAR(25) NOT NULL,

    CONSTRAINT course_PK PRIMARY KEY (course_id),

    CONSTRAINT course_dept_deptid_FK
        FOREIGN KEY (dept_id)
        REFERENCES DEPARTMENT(dept_id)
);


CREATE TABLE S_RESOURCE
(
    resource_id INT(12) AUTO_INCREMENT,
    course_id INT(7) NOT NULL,
    type VARCHAR(1) NOT NULL,
    title VARCHAR(150) NOT NULL,
    url VARCHAR(500) NOT NULL,
    descr TEXT,
    user_id INT(10) NOT NULL,

    CONSTRAINT rsc_resourceid_PK PRIMARY KEY (resource_id),

    CONSTRAINT rsc_course_cid_FK
        FOREIGN KEY (course_id)
        REFERENCES COURSE(course_id)
        ON DELETE CASCADE,

    CONSTRAINT rsc_type_CHK CHECK (type IN ('V','A','B','N','S','O')),
    -- V: Video
    -- A: Article
    -- B: Book
    -- N: Note
    -- S: Slide
    -- O: Other

    CONSTRAINT rsc_user_userid_FK
        FOREIGN KEY (user_id)
        REFERENCES AUTH_USER(id)
);


CREATE TABLE USER_WATCH_COURSE
(
    user_id INT(10),
    course_id INT(7),

    CONSTRAINT watchcourse_PK PRIMARY KEY (user_id, course_id),

    CONSTRAINT watch_user_userid_FK
        FOREIGN KEY (user_id)
        REFERENCES AUTH_USER(id)
        ON DELETE CASCADE,

    CONSTRAINT watch_course_cid_FK
        FOREIGN KEY (course_id)
        REFERENCES COURSE(course_id)
        ON DELETE CASCADE
);


CREATE TABLE USER_VOTE_RESOURCE
(
    user_id INT(10),
    resource_id INT(12),
    vote_type VARCHAR(1) NOT NULL,

    CONSTRAINT vote_uid_rid_PK PRIMARY KEY (user_id, resource_id),

    CONSTRAINT vote_votetype_CHK CHECK (vote_type IN ('U','D')),

    CONSTRAINT vote_user_userid_FK
        FOREIGN KEY (user_id)
        REFERENCES AUTH_USER(id)
        ON DELETE CASCADE,

    CONSTRAINT vote_rsc_rscid_FK
        FOREIGN KEY (resource_id)
        REFERENCES S_RESOURCE(resource_id)
        ON DELETE CASCADE
);


CREATE TABLE USER_REPORT_RESOURCE
(
    report_id INT(12) AUTO_INCREMENT, 
    user_id INT(10),
    resource_id INT(12),
    report_date DATE NOT NULL DEFAULT (CURRENT_DATE),
    descr VARCHAR(500),

    CONSTRAINT report_PK PRIMARY KEY (report_id),

    CONSTRAINT report_user_userid_FK
        FOREIGN KEY (user_id)
        REFERENCES AUTH_USER(id)
        ON DELETE SET NULL,

    CONSTRAINT report_rsc_rscid_FK
        FOREIGN KEY (resource_id)
        REFERENCES S_RESOURCE(resource_id)
        ON DELETE CASCADE
);

CREATE VIEW VOTES AS
SELECT
    resource_id,
    count(IF(vote_type='U', 1, NULL)) AS upvotes,
    count(IF(vote_type='D', 1, NULL)) AS downvotes
FROM USER_VOTE_RESOURCE
GROUP BY resource_id;