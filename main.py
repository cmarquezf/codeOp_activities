import psycopg2

conn = psycopg2.connect(
database="Company",
host="localhost",
user="postgres",
password="carmen",
port="5432")

cursor = conn.cursor()  


#1. How many projects are the IT, Marketing and HR departments working on?

cursor.execute('''SELECT COUNT(p."project_ID"), j."department"
    FROM "Employees" e
    LEFT JOIN "Jobs" j ON e."job_code" = j."job_code"
    LEFT JOIN "Projects" p ON e."project_ID" = p."project_ID"
    GROUP BY j."department";''')
               
rows = cursor.fetchall()

conn.commit()

for row in rows:
    print (f'There are {row[0]} people working in {row[1]}')


#2. How many projects are in progress, completed, or not started?

cursor.execute('''SELECT COUNT(p."project_ID"), s."project_status"
    FROM "Projects" p
    LEFT JOIN "Status" s ON p."status_ID" = s."status_ID"
    GROUP BY s."project_status";''')
rows = cursor.fetchall()
conn.commit()
for row in rows:
    print (f'There are {row[0]} projects {row[1]}')

# 3. How many employees are there for each skill?

cursor.execute('''SELECT COUNT(e."employee_ID"), j."skill"
    FROM "Employees" e
    LEFT JOIN "Jobs" j ON e."job_code" = j."job_code"
    GROUP BY j."skill";''')

rows = cursor.fetchall()
conn.commit()
for row in rows:
    print (f'There are {row[0]} employees with the  {row[1]} skill')

#4. Which employees live in the postal code `08094`? Show only the employee names.

cursor.execute('''SELECT "employee_name"
    FROM "Employees" 
    WHERE employee_address LIKE '%8094%';''')

rows = cursor.fetchall()
conn.commit()
for row in rows:
    print (row[0])


#5. Which employees are currently assigned to specific projects? Show the employee name and project name.

cursor.execute('''SELECT e."employee_name", p."project_name"
    FROM "Employees" e
    LEFT JOIN "Projects" p ON e."project_ID" = p."project_ID";''')

rows = cursor.fetchall()
conn.commit()
print ()
for row in rows:
    print (row)

#6. Provide information about the projects related to the 'Mobile App Launch' initiative.

cursor.execute('''SELECT p."project_name", s."project_status"
    FROM "Projects" p
    INNER JOIN "Status" s ON p."status_ID" = s."status_ID"
    WHERE p."project_name" = 'Mobile App Launch';''')

rows = cursor.fetchall()
conn.commit()

cursor.execute('''SELECT p."project_name", COUNT(e.employee_ID)
    FROM "Employees" e
    LEFT JOIN "Jobs" j ON e."job_code" = j."job_code"
    LEFT JOIN "Projects" p ON e."project_ID" = p."project_ID"
    LEFT JOIN "Status" s ON p."status_ID" = s."status_ID"
    GROUP BY p.project_name
    HAVING p.project_name = 'Mobile App Launch';''')

rows2 = cursor.fetchall()
conn.commit()

for row in rows:
    print (f'The project {row[0]} is in status {row[1]}')

for row in rows2:
    print (f'The project {row[0]} has {row[1]} employees working on it')

# 7. What skills are most in demand for the projects in progress?
cursor.execute('''SELECT j."skill", COUNT(j."skill")
    FROM "Employees" e
    LEFT JOIN "Jobs" j ON e."job_code" = j."job_code"
    LEFT JOIN "Projects" p ON e."project_ID" = p."project_ID"
    LEFT JOIN "Status" s ON p."status_ID" = s."status_ID"
    GROUP BY j."skill", s.project_status
    HAVING s.project_status = 'In Progress'
    ORDER BY COUNT(j."skill") DESC;''')

rows = cursor.fetchall()
conn.commit()

for row in rows:
    print (f'The skill {row[0]} is needed in {row[1]} projects')

#8. How many employees have completed their projects, and how many are still in progress?

cursor.execute('''SELECT s.project_status, COUNT(e."employee_ID") 
    FROM "Employees" e
    LEFT JOIN "Projects" p ON e."project_ID" = p."project_ID"
    LEFT JOIN "Status" s ON p."status_ID" = s."status_ID"
    GROUP BY s."project_status"
    HAVING s.project_status = 'Completed' OR s.project_status = 'In Progress' ;''')

rows = cursor.fetchall()
conn.commit()

for row in rows:
    print (f'T {row[1]} employees have projects that are {row[0]}.')

#9. What is the distribution of project statuses within each department?

cursor.execute('''SELECT j."department", s."project_status", COUNT(s."project_status")
    FROM "Employees" e
    LEFT JOIN "Jobs" j ON e."job_code" = j."job_code"
    LEFT JOIN "Projects" p ON e."project_ID" = p."project_ID"
    LEFT JOIN "Status" s ON p."status_ID" = s."status_ID"
    GROUP BY j."department", s."project_status"
    ORDER BY j."department", s."project_status"
    ;''')

rows = cursor.fetchall()
conn.commit()

for row in rows:
    print (row)

# 10. Find Employees with Programming Skills Working on In-Progress Projects. Show only the employee name, department, and project name.

cursor.execute('''SELECT e."employee_name", j."department", p."project_name"
    FROM "Employees" e
    LEFT JOIN "Jobs" j ON e."job_code" = j."job_code"
    LEFT JOIN "Projects" p ON e."project_ID" = p."project_ID"
    LEFT JOIN "Status" s ON p."status_ID" = s."status_ID"
    WHERE j."skill" = 'Programming' AND s."project_status" = 'In Progress'
    ;''')

rows = cursor.fetchall()
conn.commit()

for row in rows:
    print (row)

conn.close()
cursor.close()