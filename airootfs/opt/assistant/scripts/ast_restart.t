#!/bin/bash

RESTART_ASTS="/opt/assistant/scripts/runasts.sh --restart"
PGREP="/usr/bin/pgrep"
ASTSD="asts"
if ! $PGREP ${ASTSD}; then
   $RESTART_ASTS
fi

exit 0