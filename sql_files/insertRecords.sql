/*
    Abdulaziz Faraj, 2152135999
	Abdullah Alosaimi, 2172131914
	Mohamad Selman, 2181156265

	CS470_Project_CSHUB
*/

INSERT INTO DEPARTMENT VALUES(0418, 'Computer Science');
INSERT INTO DEPARTMENT VALUES(0410, 'Math');
INSERT INTO DEPARTMENT VALUES(0430, 'Physics');
INSERT INTO DEPARTMENT VALUES(0480, 'Statistics');
INSERT INTO DEPARTMENT VALUES(0490, 'Biological Sciences');
INSERT INTO DEPARTMENT VALUES(0420, 'Chemistry');
INSERT INTO DEPARTMENT VALUES(0610, 'Electrical Engineering');
INSERT INTO DEPARTMENT VALUES(0612, 'Computer Engineering');
INSERT INTO DEPARTMENT VALUES(0620, 'Civil Engineering');
INSERT INTO DEPARTMENT VALUES(1020, 'Accounting');

INSERT INTO COURSE VALUES(0418, 0418111, 'Discrete Math');
INSERT INTO COURSE VALUES(0418, 0418141, 'Programming I');
INSERT INTO COURSE VALUES(0418, 0418321, 'OS');
INSERT INTO COURSE VALUES(0418, 0418220, 'Programming in C');
INSERT INTO COURSE VALUES(0418, 0418201, 'Data Structures');
INSERT INTO COURSE VALUES(0418, 0418211, 'Theory of Computation I');
INSERT INTO COURSE VALUES(0418, 0418223, 'Systems Programming');
INSERT INTO COURSE VALUES(0418, 0418346, 'Declarative Programming');
INSERT INTO COURSE VALUES(0418, 0418335, 'Web Programming');
INSERT INTO COURSE VALUES(0418, 0418331, 'Computer Network');

INSERT INTO S_RESOURCE VALUES(1, 0418331, 'V', 'Playlist {Epic Networks Lab}', 'youtube.com/playlist?list=PLo80JwUm6hSSwGLJmS_quaeJgx9SILLiI', NULL, 2);
INSERT INTO S_RESOURCE VALUES(2, 0418331, 'V', 'Playlist - Security {Epic Networks Lab}', 'youtube.com/playlist?list=PLo80JwUm6hSRRepHaA3iDoxYkZCTAAVTX', NULL, 2);
INSERT INTO S_RESOURCE VALUES(3, 0418331, 'V', 'Playlist {Jim Kurose}', 'gaia.cs.umass.edu/kurose_ross/online_lectures.htm', NULL, 2);
INSERT INTO S_RESOURCE VALUES(4, 0418331, 'A', 'Protocols involved in requesting a web page', 'www.cnblogs.com/RDaneelOlivaw/p/14617358.html', NULL, 2);
INSERT INTO S_RESOURCE VALUES(5, 0418321, 'S', 'Useful slides', 'www.cs.auckland.ac.nz/courses/compsci340s2c/lectures', NULL, 2);
INSERT INTO S_RESOURCE VALUES(6, 0418321, 'N', 'Course Notes by Prof. John Bell', 'www.cs.uic.edu/~jbell/CourseNotes/OperatingSystems', NULL, 2);
INSERT INTO S_RESOURCE VALUES(7, 0418346, 'O', 'SML Book Solutions', 'www.cl.cam.ac.uk/~lp15/MLbook/exercises', NULL, 2);
INSERT INTO S_RESOURCE VALUES(8, 0418346, 'B', 'FP @ CMU', 'www.cs.cmu.edu/~15150/resources.html#texts-resources', NULL, 2);
INSERT INTO S_RESOURCE VALUES(9, 0418346, 'O', 'Prolog tutorial', 'cseweb.ucsd.edu/classes/fa09/cse130/misc/prolog/prolog_tutorial.pdf', NULL, 2);
INSERT INTO S_RESOURCE VALUES(10, 0418346, 'B', 'Learn Prolog Now!', 'www.let.rug.nl/bos/lpn//lpnpage.php?pageid=online', NULL, 2);

INSERT INTO USER_WATCH_COURSE VALUES(2, 0418211);

INSERT INTO USER_VOTE_RESOURCE VALUES(2, 1, 'U');
INSERT INTO USER_VOTE_RESOURCE VALUES(2, 2, 'U');
INSERT INTO USER_VOTE_RESOURCE VALUES(2, 3, 'U');
INSERT INTO USER_VOTE_RESOURCE VALUES(2, 4, 'U');
INSERT INTO USER_VOTE_RESOURCE VALUES(2, 5, 'U');
INSERT INTO USER_VOTE_RESOURCE VALUES(2, 6, 'U');
INSERT INTO USER_VOTE_RESOURCE VALUES(2, 7, 'U');
INSERT INTO USER_VOTE_RESOURCE VALUES(2, 8, 'U');
INSERT INTO USER_VOTE_RESOURCE VALUES(2, 9, 'U');
INSERT INTO USER_VOTE_RESOURCE VALUES(2, 10, 'U');

