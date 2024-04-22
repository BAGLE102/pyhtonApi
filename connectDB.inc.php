<?php


// 設定資料庫連接參數
$servername = "210.240.202.114\NHU-1200487-,1443"; // MySQL 伺服器名稱
$connectionOptions = array(
    "Database" => "Trash", // 数据库名称
    "Uid" => "sa", // 用户名
    "PWD" => "ji3ao6u.3au/6y4" // 密码
);

$conn = sqlsrv_connect($serverName, $connectionOptions);




//設定萬國碼
$conn ->set_charset('utf8');

// 檢查連接狀態
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

?>
