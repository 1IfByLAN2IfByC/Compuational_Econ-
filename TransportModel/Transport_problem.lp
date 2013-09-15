\* Canning Distribution Problem *\
Minimize
OBJ: Route_SD_Chi + 2 Route_SD_NY + 3 Route_SD_Top + Route_Sea_Chi
 + 5 Route_Sea_NY + 5 Route_Sea_Top
Subject To
_C1: Route_Sea_Chi + Route_Sea_NY + Route_Sea_Top <= 1000
_C2: Route_SD_Chi + Route_SD_NY + Route_SD_Top <= 4000
_C3: Route_SD_Chi + Route_Sea_Chi >= 500
_C4: Route_SD_NY + Route_Sea_NY >= 1000
_C5: Route_SD_Top + Route_Sea_Top >= 200
Bounds
0 <= Route_SD_Chi
0 <= Route_SD_NY
0 <= Route_SD_Top
0 <= Route_Sea_Chi
0 <= Route_Sea_NY
0 <= Route_Sea_Top
Generals
Route_SD_Chi
Route_SD_NY
Route_SD_Top
Route_Sea_Chi
Route_Sea_NY
Route_Sea_Top
End
