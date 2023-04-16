import json

class GrafanalibEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_json_data'):
            return obj.to_json_data()
        return super(GrafanalibEncoder, self).default(obj)

from grafanalib.core import (
    Dashboard, Graph, Row, Target, Time, YAxes, YAxis, DataSourceInput,
    Template, SingleStat, Gauge, Templating
)


# Variables
datasource_variable = Template(
    name="DS_PROMETHEUS",
    dataSource="prometheus",
    query="prometheus",
    type="datasource"
)

# Panels
cpu_usage_graph = Graph(
    title="CPU Usage",
    dataSource="$DS_PROMETHEUS",
    targets=[
        Target(
            expr='100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)',
            refId='A'
        )
    ],
    yAxes=YAxes(
        left=YAxis(format="percent", label="CPU usage"),
        right=YAxis(format="short")
    )
)

memory_usage_graph = Graph(
    title="Memory Usage",
    dataSource="$DS_PROMETHEUS",
    targets=[
        Target(
            expr='(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100',
            refId='A'
        )
    ],
    yAxes=YAxes(
        left=YAxis(format="percent", label="Memory usage"),
        right=YAxis(format="short")
    )
)

disk_usage_graph = Graph(
    title="Disk Usage",
    dataSource="$DS_PROMETHEUS",
    targets=[
        Target(
            expr='(node_filesystem_size_bytes{fstype!="rootfs",fstype!~"tmpfs|overlay"} - node_filesystem_free_bytes{fstype!="rootfs",fstype!~"tmpfs|overlay"}) / node_filesystem_size_bytes{fstype!="rootfs",fstype!~"tmpfs|overlay"} * 100',
            refId='A'
        )
    ],
    yAxes=YAxes(
        left=YAxis(format="percent", label="Disk usage"),
        right=YAxis(format="short")
    )
)

vm_up_time_graph = Graph(
    title="VM Up Time",
    dataSource="$DS_PROMETHEUS",
    targets=[
        Target(
            expr='node_time_seconds - node_boot_time_seconds',
            refId='A'
        )
    ],
    yAxes=YAxes(
        left=YAxis(format="s", label="Up Time"),
        right=YAxis(format="short")
    )
)

virtual_cpu_graph = Graph(
    title="Virtual CPU",
    dataSource="$DS_PROMETHEUS",
    targets=[
        Target(
            expr='sum(node_cpu_seconds_total{mode!="idle"})',
            refId='A'
        )
    ],
    yAxes=YAxes(
        left=YAxis(format="short", label="Virtual CPU"),
        right=YAxis(format="short")
    )
)

ram_available_graph = Graph(
    title="RAM Available",
    dataSource="$DS_PROMETHEUS",
    targets=[
        Target(
            expr='node_memory_MemAvailable_bytes',
            refId='A'
        )
    ],
    yAxes=YAxes(
        left=YAxis(format="bytes", label="RAM Available"),
        right=YAxis(format="short")
    )
)

memory_available_graph = Graph(
    title="Memory Available",
    dataSource="$DS_PROMETHEUS",
    targets=[
        Target(
            expr='node_memory_MemFree_bytes',
            refId='A'
        )
    ],
    yAxes=YAxes(
        left=YAxis(format="bytes", label="Memory Available"),
        right=YAxis(format="short")
    )
)

# Rows
row1 = Row(panels=[cpu_usage_graph, memory_usage_graph, disk_usage_graph])
row2 = Row(panels=[vm_up_time_graph, virtual_cpu_graph, ram_available_graph, memory_available_graph])

# Dashboard
dashboard = Dashboard(
    title="System Monitoring",
    rows=[row1, row2],
    time=Time(start="now-1h", end="now"),
    templating=Templating(list=[datasource_variable]),
)

# Generate JSON and print it
with open("system-monitoring.json", "w") as outfile:
    json.dump(dashboard, outfile, cls=GrafanalibEncoder)
