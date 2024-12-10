sudo nmap -sn 10.216.13.0/24 > /home/titan/bala/allIP.txt

awk '/Nmap scan report for/ {
    if ($5 == "jlrcccm2.apac.jlrint.com") {
        $5 = "jlrcccm2";
        print $5, $6;
    } else if ($5 == "jlrcccm3-Precision-5540.apac.jlrint.com") {
        $5 = "jlrcccm3-sarvesh";
        print $5, $6;
    } else if ($5 == "jlrcccm3-Precision-5540-010216013044.apac.jlrint.com") {
        $5 = "jlrcccm3";
        print $5, $6;
    } else if ($5 == "jlrcccm-rig74.apac.jlrint.com") {
        $5 = "jlrcccm";
        print $5, $6;
    } else if ($5 == "jlrcccmandroid-Precision-7780.apac.jlrint.com") {
        $5 = "jlrcccm-android";
        print $5, $6;
    } else if ($5 == "jlr4inlmjs09453.apac.jlrint.com") {
        $5 = "initial-bala";
        print $5, $6;
    } 
}' /home/titan/bala/allIP.txt > /home/titan/bala/reqIP.txt

python update_data.py
