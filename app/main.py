import logging
import time
from fastapi import FastAPI, Request, Response, status
from pydantic import BaseModel

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
)
logger = logging.getLogger("opsrelay")

app = FastAPI(title="OpsRelay Microservice")

# Internal state & metrics
is_healthy = True
request_count = 0
error_count = 0

class LogLevelPayload(BaseModel):
    level: str  # e.g., "DEBUG", "INFO", "WARNING", "ERROR"

# Middleware: Request timing & telemetry
@app.middleware("http")
async def log_requests(request: Request, call_next):
    global request_count, error_count
    request_count += 1
    start_time = time.time()
    
    response = await call_next(request)
    duration = round((time.time() - start_time) * 1000, 2)
    
    if response.status_code >= 500:
        error_count += 1
        logger.error(f"Method: {request.method} Path: {request.url.path} Status: {response.status_code} Duration: {duration}ms")
    else:
        logger.info(f"Method: {request.method} Path: {request.url.path} Status: {response.status_code} Duration: {duration}ms")
        
    return response

@app.get("/health")
def health_check(response: Response):
    if not is_healthy:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"status": "unhealthy", "reason": "Chaos injected"}
    return {"status": "healthy", "version": "1.1.0"}

@app.get("/metrics")
def get_metrics():
    """Prometheus-style telemetry metrics endpoint."""
    return {
        "total_requests": request_count,
        "total_errors": error_count,
        "error_rate_pct": round((error_count / request_count * 100), 2) if request_count > 0 else 0.0,
        "system_status": "healthy" if is_healthy else "degraded"
    }

@app.post("/log-level")
def set_log_level(payload: LogLevelPayload, response: Response):
    """Dynamically adjust log verbosity without restarting the container."""
    level_str = payload.level.upper()
    numeric_level = getattr(logging, level_str, None)
    if not isinstance(numeric_level, int):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": f"Invalid log level: {payload.level}"}
    
    logger.setLevel(numeric_level)
    logger.warning(f"Log level dynamically changed to {level_str}")
    return {"message": f"Log level updated to {level_str}"}

@app.post("/chaos")
def trigger_chaos():
    global is_healthy
    is_healthy = False
    logger.critical("Chaos triggered via API POST /chaos!")
    return {"message": "Chaos triggered! App is now returning HTTP 500 on /health."}

@app.post("/recover")
def recover_app():
    global is_healthy
    is_healthy = True
    logger.info("Application state recovered to healthy.")
    return {"message": "App state recovered to healthy."}