from fastapi import FastAPI

from src.router.auth import router as AuthRouter
from src.router.user import router as UserRouter
from src.router.teams import router as TeamsRouter
from src.router.matches import router as MatchesRouter
from src.router.venue import router as VenueRouter

app = FastAPI(title="Cric(More)Info", version="1.0")

app.include_router(AuthRouter)
app.include_router(UserRouter)
app.include_router(TeamsRouter)
app.include_router(MatchesRouter)
app.include_router(VenueRouter)

@app.get('/')
def health():
    return {
        'message' : "Your application is up and running"
    }
