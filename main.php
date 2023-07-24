<?php

ini_set('display_errors', '1');
ini_set('display_startup_errors', '1');
error_reporting(E_ALL);

require_once "./src/Out/Generator.php";
require_once "./src/Parse/Parser.php";

// first write content of pdf file for running python file
try {
    $pythonFile = './src/In/getContentPdf.py';
    $command = 'python ' . $pythonFile;
    $output = shell_exec($command);
} catch (Exception $e) {
    echo "Hata oluştu: " . $e->getMessage();
    exit;
}

// get file txt from folder
$files = glob('./tmp/*.txt');
if (empty($files)) {
    echo "There is no file with filemask, /tmp/*"; 
}

foreach ($files as $file) {

    //unlink($file);
}

