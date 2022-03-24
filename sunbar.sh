#!/usr/bin/env bash
# exit on error, exit on undefined variables, error on failing pipe commands
set -euo pipefail

# bash >= 4.4
if [[ ${BASH_VERSINFO[0]} -gt 4 ||
  ${BASH_VERSINFO[0]} -eq 4 && ${BASH_VERSINFO[1]} -ge 4 ]] \
  ; then
  # error on commands in command substitutions
  shopt -s inherit_errexit
fi

get_script_dir() {
  # https://stackoverflow.com/a/246128
  local SOURCE DIR
  SOURCE="${BASH_SOURCE[0]}"
  while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
    DIR="$(cd -P "$(dirname "$SOURCE")" > /dev/null 2>&1 && pwd)"
    SOURCE="$(readlink "$SOURCE")"
    [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
  done
  DIR="$(cd -P "$(dirname "$SOURCE")" > /dev/null 2>&1 && pwd)"
  echo "$DIR"
}

(
  cd "$(get_script_dir)"
  export PIPENV_QUIET=1
  exec pipenv run "$(get_script_dir)/sunbar.py" "$@"
)
