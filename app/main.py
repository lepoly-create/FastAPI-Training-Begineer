from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.config import settings
from app.core.database import Base, engine
from app.views.article import articles_views

app = FastAPI()

app.mount("/public", StaticFiles(directory=settings.STATIC_FILES_DIR), name="public")

templates = Jinja2Templates(directory="app/templates")


Base.metadata.create_all(bind=engine)
"""app.mount , est une route qui va repondre a l'URL /static et qui servira, sous cette addresse,
 les fichiers que nous mettrons dans le repertoire public/ .
 nous nommons ainsi cette route public (name="public"), car nous aurons 
 besoin de l'appeller par son nom pour nous en servir un peu plus loin"""


"""Nous creons alors un objet templates qui va nous permettre de créer
de l'HTML avec le moteur de template Jinja2, ce objet ira chercher ses 
templates dans le repertoire (app/templates/)"""



"""ici nous avons rexupere l'objet request par notre methode root
, ce objet est fourni par starlette qui est le FrameWork sur lequel FastAPI est basé.
il nous permet d'obtenir les informations sur la requéte: URL dorigine, cookies, headers,..."""


app.include_router(articles_views, tags=["Articles"])


@app.get("/", include_in_schema=False)
async def root(request: Request):
    return templates.TemplateResponse(request, "home.html")
