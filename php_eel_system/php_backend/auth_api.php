<?php
// php_backend/auth_api.php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST, GET, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");
header('Content-Type: application/json');

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// User database
$users_db = [
    "admin" => ["password" => "1234", "name" => "admin"],
    "user"  => ["password" => "pass",  "name" => "Regular User"],
];

// Get POST data
$raw = file_get_contents('php://input');
$data = json_decode($raw, true) ?? [];

$username = isset($data['username']) ? trim($data['username']) : '';
$password = isset($data['password']) ? trim($data['password']) : '';

// Validate credentials
if (isset($users_db[$username]) && $users_db[$username]['password'] === $password) {
    echo json_encode([
        "success" => true,
        "message" => "Welcome, " . $users_db[$username]['name'] . "!",
    ]);
} else {
    http_response_code(401);
    echo json_encode([
        "success" => false,
        "message" => "Invalid credentials!",
    ]);
}
?>