<?php

// Connect to the SQLite database
$db = new PDO('sqlite:students.db');

// Create a query to select all students with role "student"
$query = 'SELECT * FROM students WHERE role = "student"';

// Execute the query
$results = $db->query($query);

// Iterate through the results and create an array of students
$registered_students = [];
foreach ($results as $row) {
  $registered_students[] = [
    'id' => $row['id'],
    'name' => $row['name'],
    'email' => $row['email'],
  ];
}

// Display the list of students
echo '<table class="table table-bordered">';
echo '<thead>';
echo '<tr>';
echo '<th>Student ID</th>';
echo '<th>Student Name</th>';
echo '<th>Email</th>';
echo '</tr>';
echo '</thead>';
echo '<tbody>';

// Loop through the list of students and add a row for each student
foreach ($registered_students as $student) {
  echo '<tr>';
  echo '<td>' . $student['id'] . '</td>';
  echo '<td>' . $student['name'] . '</td>';
  echo '<td>' . $student['email'] . '</td>';
  echo '</tr>';
}

echo '</tbody>';
echo '</table>';

?>
