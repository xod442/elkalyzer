#!/bin/bash

# Unset the HTTP_PROXY and HTTPS_PROXY environment variables
unset HTTP_PROXY
unset HTTPS_PROXY

# Optionally unset lowercase versions as well, as they are sometimes used
unset http_proxy
unset https_proxy

echo "HTTP_PROXY and HTTPS_PROXY environment variables have been unset."
