"""Router for the Home of the Website"""
import fastapi
from db.database import get_db
from fastapi import Depends
from fastapi.responses import HTMLResponse
from schemes import Allergies
from schemes import scheme_filter
from schemes import scheme_cuisine
from schemes import scheme_allergie
from schemes import scheme_rest
from schemes.scheme_user import UserBase
from services import service_res
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from typing import Union
from typing import List


templates = Jinja2Templates("templates")
router = fastapi.APIRouter()


@router.get("/findrestaurant", response_class=HTMLResponse)
async def findrestaurant(
    request: Request,
    rating: int,
    costs: float,
    radius: int,
    lat: str,
    lng: str,
    cuisine: Union[str, None] = None,
    allergies: Union[str, None] = None,
    db_session: Session = Depends(get_db)
):

    # cuisine:str zum Cuisine-Array machen
    if cuisine is not None:
        cuisine_list = [scheme_cuisine.PydanticCuisine(name=cuisine) for cuisine in cuisine.split(",")]
    else:
        cuisine_list = [scheme_cuisine.PydanticCuisine(name="Essen")]
    allergies_list = allergies
    if allergies is not None:
        allergies_list = [scheme_allergie.PydanticAllergies(name=allergie) for allergie in allergies.split(",")]
    rest_filter = scheme_filter.FilterRest(
        cuisines=cuisine_list,
        allergies=allergies_list,
        rating=rating,
        costs=costs,
        radius=radius * 1000,
        location=scheme_rest.LocationBase(lat=lat, lng=lng),
    )
    mock_user = UserBase(email="example@gmx.de")
    rest_filter_db = scheme_filter.FilterRestDatabase(cuisines=rest_filter.cuisines, allergies=rest_filter.allergies,
                                                      rating=rest_filter.rating, costs=rest_filter.costs, radius=rest_filter.radius, zipcode="88045")
    service_res.update_rest_filter(db_session=db_session, filter_updated=rest_filter_db, user=mock_user)
    restaurant = service_res.search_for_restaurant(db_session=db_session, user=mock_user, user_f=rest_filter)
    return templates.TemplateResponse(
        "restaurant/restaurant_result.html", {"request": request, "restaurant": restaurant}
    )


def str_to_array(cuisines: str):
    return cuisines.split(',')
