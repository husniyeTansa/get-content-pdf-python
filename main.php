<?php

/**
 * PHP Version >= PHP 7.4
 *
 * @category Mapping
 * @package  MidpointYbpOrders
 * @license  MAP E-Commerce and Data Services Inc.
 * @link     https://www.map.com.tr
 */

require_once __DIR__ . '/vendor/autoload.php';

// ---------------------------------------------------------------------------------------------------------------------

use Midpoint\Ybp\Out\Generator;
use Midpoint\Ybp\Parser\Parser;

ini_set('display_errors', '1');
ini_set('display_startup_errors', '1');
error_reporting(E_ALL);

// ---------------------------------------------------------------------------------------------------------------------

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
$files = glob('./tmp-txt/*.txt');
if (empty($files)) {
    echo "There is no file with filemask, /tmp/*"; 
}

foreach ($files as $file) {

    $parser = new Parser();
    $order_data = $parser->parseContent($file);
    print_r($order_data); die;
    $generator = new Generator();
    $output = $generator->generateD96A($orderData);

    print_r($output);

    die;
    //unlink($file);
}

