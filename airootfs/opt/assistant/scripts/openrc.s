#!/sbin/openrc-run

command="/opt/assistant/scripts/runasts.sh"
pidfile="/var/run/assistant.pid"
HOME=/root
export HOME

depend () {
	need net
}

stop() {
	/opt/assistant/scripts/runasts.sh --stop
}

restart () {
	/opt/assistant/scripts/runasts.sh --restart
}
