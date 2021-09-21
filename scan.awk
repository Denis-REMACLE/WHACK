$1 == "BSS" {
    MAC = $2
    wifi[MAC]["mac"] = MAC
    wifi[MAC]["enc"] = "Open"
}
$1 == "SSID:" {
    wifi[MAC]["SSID"] = $2
}
$1 == "BSSID:" {
    wifi[MAC]["BSSID"] = $NF
}
$1 == "signal:" {
    wifi[MAC]["sig"] = $2 " " $3
}
$1 == "WPA:" {
    wifi[MAC]["enc"] = "WPA"
}
$1 == "WEP:" {
    wifi[MAC]["enc"] = "WEP"
}
END {
    for (w in wifi) {
        printf "%s,%s,%s\n",wifi[w]["SSID"],wifi[w],wifi[w]["enc"]
    }
}