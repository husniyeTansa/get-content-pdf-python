<?php

namespace Midpoint\Ybp\Out;

use Midpoint\Ybp\Helpers\Helper;
use DateTime;
use Edi\Edifact\D96A\Orders;
use Edi\Edifact\D96A\Segment\BGM;
use Edi\Edifact\D96A\Segment\CUX;
use Edi\Edifact\D96A\Segment\DTM;
use Edi\Edifact\D96A\Segment\IMD;
use Edi\Edifact\D96A\Segment\LIN;
use Edi\Edifact\D96A\Segment\NAD;
use Edi\Edifact\D96A\Segment\PAC;
use Edi\Edifact\D96A\Segment\PIA;
use Edi\Edifact\D96A\Segment\PRI;
use Edi\Edifact\D96A\Segment\QTY;
use Edi\Edifact\D96A\Segment\RFF;
use Edi\Edifact\D96A\Segment\UNH;
use Edi\Edifact\D96A\Segment\UNS;
use Edi\Edifact\D96A\SegmentGroup\SG2;
use Edi\Edifact\D96A\SegmentGroup\SG25;
use Edi\Edifact\D96A\SegmentGroup\SG28;
use Edi\Edifact\D96A\SegmentGroup\SG3;
use Edi\Edifact\D96A\SegmentGroup\SG30;
use Edi\Edifact\D96A\SegmentGroup\SG7;
use Edi\Edifact\Interchange;
use Edi\Edifact\UNA;
use Edi\Edifact\UNB;
use Exception;

/**
 * Class Generator
 *
 * @package A101\Nivea\Out
 */
class Generator
{
    /**
     * @var string
     */
    protected string $midpoint = "9044444094001";
    /**
     * @var string
     */
    protected string $ybpGln = "9011111941028";

    /**
     * @param $data
     *
     * @return Interchange
     */
    public function generateD96A($data)
    {
        $interchange = new Interchange();
        $interchange->setUna(new UNA());
        $unb = new UNB();
        $interchange->setUnb(
            $unb
                ->setSyntaxIdentifier('UNOG')
                ->setSyntaxVersionNumber('2')
                ->setPreparationDate(new DateTime())
                ->setIcnSenderId($this->midpoint)
                ->setIcnSenderQualifier('14')
                ->setIcnReceiverId($this->ybpGln)
                ->setIcnReceiverQualifier('14')
                ->setIcnControlReference($data["orderNumber"])
                ->setApplicationRef('ORDERS')
        );
        $orders = new Orders();
        $unh = new UNH();
        $orders->setUnh(
            $unh
                ->setMessageReferenceNumber('1')
                ->setMessageType('ORDERS')
                ->setMessageVersionNumber('D')
                ->setMessageReleaseNumber('96A')
                ->setMessageControllingAgency('UN')
                ->setAssociationAgencyCode('EAN008')
                ->setMessageType('ORDERS')
        );
        $bgm = new BGM();
        $orders->setBgm(
            $bgm
                ->setMessageNameCode('220')
                ->setMessageNumber($data["orderNumber"])
                ->setMessageFunctionCode('9')
        );
        $dtm = new DTM();
        $orders->insertDtm(
            $dtm
                ->setPeriodQualifier('137')
                ->setPeriod(DateTime::createFromFormat('Ymd', $data["orderDate"]))
                ->setPeriodFormatQualifier('102')
        );
        $sg2 = new SG2();
        $nad = new NAD();
        $sg2->setNad(
            $nad
                ->setPartyQualifier('SU')
                ->setPartyIdentifier($this->ybpGln)
                ->setPartyCodeListAgency('9')
        );
        $sg2 = new SG2();
        $nad = new NAD();
        $orders->insertSg2(
            $sg2->setNad(
                $nad
                    ->setPartyQualifier('BY')
                    ->setPartyIdentifier($this->midpoint)
                    ->setPartyCodeListAgency('9')
            )
        );
        $sg2 = new SG2();
        $nad = new NAD();
        $orders->insertSg2(
            $sg2->setNad(
                $nad
                    ->setPartyQualifier('DP')
                    ->setPartyIdentifier($data["deliveryPoint"])
                    ->setPartyCodeListAgency('9')
            )
        );
        $sg7 = new SG7();
        $cux = new CUX();
        $sg7->setCux(
            $cux
                ->setDetailQualifier('2')
                ->setCode('TRY')
                ->setQualifier('9')
        );
        $orders->insertSg7($sg7);

        foreach ($data["lines"] as $i => $orderLine) {
            if (!isset($orderLine['Line-Item'])) {
                $orderLine['Line-Item'] = $orderLine;
            }
            $orderLine['Line-Item']['itemDescription'] = trim(
                str_replace(
                    ['®', '™', ".", '°', '–'],
                    ['', '', '', '', '-'],
                    $orderLine["itemDescription"]
                )
            );
            $lineItem = $orderLine['Line-Item'];
            $sg25 = new SG25();
            $lin = new LIN();
            $sg25->setLin(
                $lin
                    ->setLineItemNumber($i + 1)
                    ->setItemNumber($lineItem['ean'])
                    ->setItemNumberTypeCode('EN')
            );
            $pia = new PIA();
            $sg25->insertPia(
                $pia->setProductIdQualifier(1)
                    ->setItemNumber($lineItem['buyerPartNumber'])
                    ->setItemNumberTypeCode('BP')
            );
            try {
                $imd = new IMD();
                $sg25->insertImd(
                    $imd
                        ->setItemDescriptionType('F')
                        ->setItemDescription(mb_substr(Helper::fixTurkishChar($lineItem['itemDescription']), 0, 70))
                );
            } catch (Exception $exception) {
                echo $exception->getMessage() . PHP_EOL;
            }
            $qty = new QTY();
            $sg25->insertQty(
                $qty
                    ->setQualifier('21')
                    ->setQuantity($lineItem['quantity'])
            );
            $orders->insertSg25($sg25);

            $dtm = new DTM();
            $sg25->insertDtm(
                $dtm
                    ->setPeriodQualifier("265")
                    ->setPeriod(DateTime::createFromFormat('Ymd', $lineItem["deliveryDate"]))
                    ->setPeriodFormatQualifier('102')
            );
        }
        $uns = new UNS();
        $interchange->insertMessage(
            $orders
                ->setUns(
                    $uns
                        ->setSectionId('S')
                )
        );

        return $interchange;
    }
}
