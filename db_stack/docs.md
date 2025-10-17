Setup telegraph to use a timescaledb: https://docs.tigerdata.com/integrations/latest/telegraf/
- try to collect all metrics.
- ```docker run --rm telegraf telegraf --input-filter cpu:mem:disk:net  --output-filter=postgresql config > telegraf.conf```

postgress could not bind to port, already in use. => https://superuser.com/questions/756933/postgresql-does-not-start-in-ubuntu-says-could-not-bind-ipv4-socket

make graphana dash for telegraf metrics: https://docs.tigerdata.com/integrations/latest/grafana/
- goal: full system dashboard: https://grafana.com/grafana/dashboards/928-telegraf-system-dashboard/


pgadmin for internal db stats + explorer: https://www.pgadmin.org/

> [!NOTE]
> Docker compose is set to use network_mode: host
> Portmapping is pointless but left in as a quick guide to active ports.
> Localhost is internal for each container, use 127.0.0.1:port

### out of scope but hella usefull.

pgbouncer for connection pooling: https://www.tigerdata.com/blog/connection-pooling-on-timescale-or-why-pgbouncer-rocks






