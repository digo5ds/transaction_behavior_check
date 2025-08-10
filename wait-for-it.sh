#!/bin/bash
# wait-for-it.sh

# https://github.com/vishnubob/wait-for-it

TIMEOUT=15
QUIET=0
WAITFORIT_HOST=
WAITFORIT_PORT=

echoerr() {
  if [ "$QUIET" -ne 1 ]; then echo "$@" 1>&2; fi
}

usage()
{
  cat << USAGE >&2
Usage:
  $0 host:port [-t timeout] [-- command args]
  -h | --help         Show this message
  -q | --quiet        Don't output any status messages
  -t | --timeout N    Timeout in seconds, zero for no timeout
  --                  Separator for command to execute
USAGE
  exit 1
}

# process arguments
while [ $# -gt 0 ]
do
  case "$1" in
    *:* )
    WAITFORIT_HOST=$(printf "%s\n" "$1"| cut -d : -f 1)
    WAITFORIT_PORT=$(printf "%s\n" "$1"| cut -d : -f 2)
    shift
    ;;
    -q | --quiet)
    QUIET=1
    shift
    ;;
    -t | --timeout)
    TIMEOUT="$2"
    if [ "$TIMEOUT" = "" ]; then break; fi
    shift 2
    ;;
    --)
    shift
    break
    ;;
    *)
    usage
    ;;
  esac
done

if [ "$WAITFORIT_HOST" = "" ] || [ "$WAITFORIT_PORT" = "" ]; then
  usage
fi

wait_for_it()
{
  if [ "$QUIET" -ne 1 ]; then echo "Waiting for $WAITFORIT_HOST:$WAITFORIT_PORT to be available..." 1>&2; fi
  
  if [ "$TIMEOUT" -gt 0 ]; then
    TIMEOUT_TIMESTAMP=$(date +%s)
    TIMEOUT_TIMESTAMP=$((TIMEOUT_TIMESTAMP + TIMEOUT))
  else
    TIMEOUT_TIMESTAMP=0
  fi
  
  while :
  do
    if [ "$TIMEOUT" -gt 0 ]; then
      CURRENT_TIMESTAMP=$(date +%s)
      if [ "$CURRENT_TIMESTAMP" -ge "$TIMEOUT_TIMESTAMP" ]; then
        echo "Timeout occurred after $TIMEOUT seconds waiting for $WAITFORIT_HOST:$WAITFORIT_PORT" 1>&2
        exit 1
      fi
    fi
    
    (echo > /dev/tcp/$WAITFORIT_HOST/$WAITFORIT_PORT) >/dev/null 2>&1
    
    if [ $? -eq 0 ]; then
      if [ "$QUIET" -ne 1 ]; then echo "$WAITFORIT_HOST:$WAITFORIT_PORT is available" 1>&2; fi
      break
    else
      sleep 1
    fi
  done
  
  return 0
}

wait_for_it