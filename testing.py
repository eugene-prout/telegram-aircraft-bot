import uuid
from bot.services import LatLong, get_flights_near_user
import wikipedia

# userpos = LatLong(latitude=51.909904, longitude=-1.139092)
# request_id = uuid.uuid4()
# get_flights_near_user(userpos, request_id)
c = wikipedia.summary("Tecnam P2008-JC")
print(c)
