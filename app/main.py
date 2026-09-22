from fastapi import FastAPI, Response, status

app = FastAPI(title="OpsRelay Microservice")

# Internal state tracking app health
is_healthy = True

@app.get("/health")
def health_check(response: Response):
    if not is_healthy:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"status": "unhealthy", "reason": "Chaos injected"}
    return {"status": "healthy", "version": "1.0.0"}

@app.post("/chaos")
def trigger_chaos():
    global is_healthy
    is_healthy = False
    return {"message": "Chaos triggered! App is now returning HTTP 500 on /health."}

@app.post("/recover")
def recover_app():
    global is_healthy
    is_healthy = True
    return {"message": "App state recovered to healthy."}