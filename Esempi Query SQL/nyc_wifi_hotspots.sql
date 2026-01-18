#Query per i nodi

SELECT DISTINCT(NTACode)
FROM nyc_wifi_hotspots
WHERE borough = %s

#Query per gli archi

SELECT n1.NTACode, n2.NTACode, COUNT(DISTINCT(n1.SSID)) as w1, COUNT(DISTINCT(n2.SSID)) as w2
FROM nyc_wifi_hotspots n1, nyc_wifi_hotspots n2
WHERE n1.NTACode < n2.NTACode and n1.borough = %s and n2.borough = %s
GROUP BY n1.NTACode, n2.NTACode