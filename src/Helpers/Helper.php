<?php

namespace Midpoint\Ybp\Helpers;

/**
 * Class Helper
 *
 * @category Mapping
 * @package  A101\Evyap\Helpers
 * @license  MAP E-Commerce and Data Services Inc.
 * @link     https://www.map.com.tr
 */
class Helper
{
    public static function toFloat($num): float
    {
        $dotPos = strrpos($num, '.');
        $commaPos = strrpos($num, ',');
        $sep = (($dotPos > $commaPos) && $dotPos) ? $dotPos :
            ((($commaPos > $dotPos) && $commaPos) ? $commaPos : false);

        if (!$sep) {
            return floatval(preg_replace("/[^0-9]/", "", $num));
        }

        return floatval(
            preg_replace("/[^0-9]/", "", substr($num, 0, $sep)) . '.' .
            preg_replace("/[^0-9]/", "", substr($num, $sep + 1, strlen($num)))
        );
    }

    /**
     * @param $string
     *
     * @return string|null
     */
    public static function charFormat(string $string): ?string
    {
        $string = self::escapeChar(trim($string));
        $length = mb_strlen($string) / 35;
        $formatted_string = null;
        for ($i = 0; $i <= ($length < 1 ? 0 : $length); $i++) {
            $formatted_string .= mb_substr($string, $i * 35, 35) . ":";
        }
        $formatted_string = rtrim($formatted_string, ":");

        return $formatted_string;
    }

    /**
     * @param $string
     *
     * @return string|string[]
     */
    public static function escapeChar(string $string)
    {
        return str_replace(["'", ":", "+", "  "], ["?'", "?:", "?+", " "], $string);
    }

    /**
     * @param string $string
     *
     * @return string|string[]
     */
    public static function fixEncoding(string $string)
    {
        $find = ["ý", "Ý", "Þ", "þ", "Ð", "ð", "&#30;", "^"];
        $replace = ["i", "I", "S", "s", "G", "g", "", ""];

        return str_replace($find, $replace, $string);
    }

    /**
     * @param string $string
     * @return string|string[]
     */
    public static function fixTurkishChar(string $string)
    {
        return str_replace(
            ["ğ", "Ğ", "ü", "Ü", "Ç", "ç", "İ", "ı", "Ş", "ş", "Ö", "ö"],
            ["g", "G", "u", "U", "C", "c", "I", "İ", "S", "s", "O", "o"],
            $string
        );
    }

    /**
     * @param int $length
     *
     * @return string
     */
    public static function generateUniqueId(int $length = 5): string
    {
        return strtoupper(bin2hex(openssl_random_pseudo_bytes($length)));
    }

    /**
     * @param $array
     * @return mixed
     */
    public static function arrayFilterRecursive($array)
    {
        foreach ($array as $key => $item) {
            is_array($item) && $array[$key] = self::arrayFilterRecursive($item);
            if (empty($array[$key])) {
                unset($array[$key]);
            }
        }
        return $array;
    }
}
