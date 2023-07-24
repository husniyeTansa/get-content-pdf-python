<?php

function setTxtContent($file)
{

    $content_file = file_get_contents($file);
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
        } elseif (empty($trimmed_line) && !$check_empty_line) {
            $content_pages[$count_page][] = "*final-address*";
            $check_empty_line = true;
        }
    }

    $edi_content = array();
    $edi_content['title'] = $content_pages[0][0];
    $edi_content['address'] = '';
    $edi_content['product'] = array();
    $order_check = 0;
    $product_check = 0;
    $temp_lines = array();

    foreach ($content_pages as $lines) {

        for ($i = 1; $i < sizeof($lines); $i++) {

            if ($order_check == 0 && $lines[$i] != '*final-address*') {
                $edi_content['address'] .= ' ' . strval($lines[$i]);
            } else if ($order_check == 0 && $lines[$i] == '*final-address*') {
                $order_check++;
            }

            if ($lines[$i] == '*final-address*') {
                continue;
            } else if ($order_check == 1) {
                $edi_content['address-detail-1'] = $lines[$i];
                $order_check++;
                continue;
            } else if ($order_check == 2) {
                $edi_content['address-detail-2'] = $lines[$i];
                $order_check++;
                continue;
            }

            if ($order_check == 3) {
                if (str_contains(strval($lines[$i]), 'Sipariş No :')) {
                    $temp = str_replace('Sipariş No :', '', $lines[$i]);
                    $edi_content['order-no'] = str_replace('«sube»', '', $temp);
                } else if (str_contains(strval($lines[$i]), 'Firma :')) {
                    $edi_content['company'] = str_replace('Firma :', '', $lines[$i]);
                } else if (str_contains(strval($lines[$i]), 'Tel :')) {
                    preg_match('/Tel\s*:\s*(\d+)\s*Faks\s*:\s*(\d+)/', $lines[$i], $matches);;
                    $edi_content['phone'] = $matches[1];
                    $edi_content['faks'] = $matches[2];
                } else if (str_contains(strval($lines[$i]), 'Notlar :')) {
                    preg_match('/Notlar\s*:\s*(.*?)\s*Sipariş Tarihi\s*:(.*?)\s*OMNİ/', $lines[$i], $matches);
                    $edi_content['note'] = $matches[1];
                    $edi_content['order-date'] = $matches[2];
                } else if (str_contains(strval($lines[$i]), 'Teslim Tarihi :')) {
                    $edi_content['delivery-date'] = str_replace('Teslim Tarihi :', '', $lines[$i]);
                } else if (str_contains(strval($lines[$i]), 'Depo Adı :')) {
                    $edi_content['store-name'] = str_replace('Depo Adı :', '', $lines[$i]);
                }
            }

            if ($order_check == 3 && str_contains(strval($lines[$i]), 'Sayfa')) {
                $order_check++;
                continue;
            }

            if ($order_check == 4 && str_contains(strval($lines[$i]), 'Toplam')) {
                $order_check++;
            }

            if ($order_check == 4) {
                if (str_contains(strval($lines[$i]), 'SK')) {
                    if (isset($temp_lines[$product_check])) {
                        $temp_lines[$product_check] .= ' ' . strval($lines[$i]);
                    } else {
                        $temp_lines[$product_check] = strval($lines[$i]);
                    }
                    $product_check++;
                } else if (str_contains(strval($lines[$i]), '%') === false) {
                    $temp_lines[$product_check] = strval($lines[$i]);
                } else {
                    $temp_lines[$product_check - 1] .= ' ' . strval($lines[$i]);
                }
            }

            if ($order_check == 5) {
                if (str_contains(strval($lines[$i]), 'G. Toplam')) {
                    $temp = str_replace('G. Toplam', '', $lines[$i]);
                    $edi_content['grand-total'] = str_replace('«genel_toplam»', '', $temp);
                } else if (str_contains(strval($lines[$i]), 'İndirim')) {
                    $edi_content['discount'] = str_replace('İndirim', '', strval($lines[$i]));
                } else if (str_contains(strval($lines[$i]), 'Ara Top.')) {
                    $edi_content['subtotal'] = str_replace('Ara Top.', '', strval($lines[$i]));
                } else if (str_contains(strval($lines[$i]), 'KDV')) {
                    $edi_content['kdv'] = str_replace('KDV', '', strval($lines[$i]));
                } else if (str_contains(strval($lines[$i]), 'Toplam')) {
                    $edi_content['sum'] = str_replace('Toplam', '', strval($lines[$i]));
                } else if (str_contains(strval($lines[$i]), 'Satınalma Yetkilisi:')) {
                    $edi_content['official'] = str_replace('Satınalma Yetkilisi:', '', strval($lines[$i]));
                }
            }
        }

        foreach ($temp_lines as $line) {
            $arr_product = array();
            $arr_line = explode(" ", $line);
            $order_check_for_pro = 0;

            foreach ($arr_line as $value) {
                if ($order_check_for_pro == 0 && str_contains($value, 'SK') === false) {
                    if (isset($arr_product['urun-adi'])) {
                        $arr_product['urun-adi'] .= ' ' . $value;
                    } else {
                        $arr_product['urun-adi'] = $value;
                    }
                } else if ($order_check_for_pro == 0 && str_contains($value, 'SK') === true) {
                    $arr_product['urun-kodu'] = $value;
                    $order_check_for_pro++;
                    continue;
                }

                if ($order_check_for_pro == 1) {
                    preg_match('/(\d+)([A-Za-z]+)/', $value, $matches);
                    if (isset($matches[1]) && isset($matches[2])) {
                        $arr_product['miktar'] = $matches[1];
                        $arr_product['birim'] = $matches[2];
                    }
                    $order_check_for_pro++;
                    continue;
                }

                if ($order_check_for_pro == 2) {
                    if (isset($arr_product['br-fiyat'])) {
                        $arr_product['br-fiyat'] .= ' ' . $value;
                        $order_check_for_pro++;
                        continue;
                    } else {
                        $arr_product['br-fiyat'] = $value;
                    }
                }

                if ($order_check_for_pro == 3 && str_contains($value, '%')) {
                    $arr_product['ind1'] = $value;
                    $order_check_for_pro++;
                    continue;
                }

                if ($order_check_for_pro == 4 && str_contains($value, '%')) {
                    $arr_product['ind2'] = $value;
                    $order_check_for_pro++;
                    continue;
                }

                if ($order_check_for_pro == 5) {
                    if (isset($arr_product['tutar'])) {
                        $arr_product['tutar'] .= ' ' . $value;
                        $order_check_for_pro++;
                        continue;
                    } else {
                        $arr_product['tutar'] = $value;
                    }
                }

                if ($order_check_for_pro == 6 && str_contains($value, '%')) {
                    $arr_product['kdv'] = $value;
                }
            }

            $edi_content['product'][] = $arr_product;
        }
    }

    $edi_content = removeExtraSpacesRecursively($edi_content);
    return $edi_content;
}

function removeExtraSpaces($value)
{
    $value = trim(@$value);
    $value = preg_replace('/\s+/', ' ', $value);

    return $value;
}

function removeExtraSpacesRecursively($array)
{
    foreach ($array as $key => $value) {
        if (is_array($value)) {
            $array[$key] = removeExtraSpacesRecursively($value);
        } else {
            $array[$key] = removeExtraSpaces($value);
        }
    }
    return $array;
}
