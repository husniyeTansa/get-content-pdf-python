<?php

ini_set('display_errors', '1');
ini_set('display_startup_errors', '1');
error_reporting(E_ALL);

$content_file = file_get_contents("./pdf_content.txt");
$content_file = explode("\n", $content_file);

$count_page = -1;
$content_pages = array();
$check_empty_line = false;

foreach ($content_file as $line) {

    $trimmed_line = trim($line);
    if (str_contains(strval($trimmed_line), 'Page')) {
        $count_page++;
    } elseif (!empty($trimmed_line)) {
        $content_pages[$count_page][] = $trimmed_line;
    } elseif(empty($trimmed_line) && !$check_empty_line){
        $content_pages[$count_page][] = "*final-address*";
        $check_empty_line = true;
    }
}
//print_r($content_pages); die;
foreach ($content_pages as $lines) {

    $edi_content = array();
    $edi_content['title'] = $lines[0];
    $edi_content['address'] = '';
    $order_check = 0;

    for ($i=1; $i<sizeof($lines); $i++) {
        
        if($order_check == 0 && $lines[$i] != '*final-address*'){
            $edi_content['address'] .= ' ' . strval($lines[$i]);
        }else if($order_check == 0 && $lines[$i] == '*final-address*'){
            $order_check++;
        }

        if($lines[$i] == '*final-address*'){
            continue;
        }else if($order_check == 1){
            $edi_content['address-detail-1'] = $lines[$i];
            $order_check++;
            continue;
        } else if($order_check == 2){
            $edi_content['address-detail-2'] = $lines[$i];
            $order_check++;
            continue;
        }

        if(str_contains(strval($lines[$i]), 'Sipariş No :')){
            $edi_content['order-no'] = $lines[$i];
        }else if(str_contains(strval($lines[$i]), 'Firma :')){

        }else if(str_contains(strval($lines[$i]), 'Tel :')){

        }else if(str_contains(strval($lines[$i]), 'Notlar :')){

        }else if(str_contains(strval($lines[$i]), 'Teslim Tarihi :')){

        }else if(str_contains(strval($lines[$i]), 'Depo Adı :')){

        }

    }

    print_r($edi_content);

}

