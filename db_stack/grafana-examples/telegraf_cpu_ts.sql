SELECT
    time AS "time",
    cpu,
    (usage_guest + usage_guest_nice + usage_system + usage_softirq + usage_irq + usage_nice + usage_iowait + usage_steal) AS cpu0
FROM
    cpu
WHERE
    cpu = 'cpu0'
    AND
    $__timeFilter(time)
ORDER BY
    time ASC
