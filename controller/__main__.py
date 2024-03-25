import sys

sys.path.append('/app')

import uvicorn

from common.config import config

if __name__ == "__main__":
    uvicorn.run(
        "controller:app",
        host=config.CONTROLLER_IP,
        port=config.CONTROLLER_HTTP_PORT,
        reload=False,
        log_level=uvicorn.config.LOG_LEVELS["warning"],
    )
