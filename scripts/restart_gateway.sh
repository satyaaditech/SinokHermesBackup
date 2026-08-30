#!/usr/bin/env bash
# Detached gateway restart — survives the gateway's own SIGTERM
sleep 4
systemctl --user restart hermes-gateway
