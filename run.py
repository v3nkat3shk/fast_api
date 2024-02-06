#!/usr/bin/env python

import uvicorn


if __name__ == '__main__':
    uvicorn.run(
        "server.main:application",
        port=8080,
        log_level="info",
        reload=True
    )