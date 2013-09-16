\* Canning Distribution Problem *\
Minimize
OBJ: 162 Route_SD_Chi + 225 Route_SD_NY + 126 Route_SD_Top + 153 Route_Sea_Chi
 + 225 Route_Sea_NY + 162 Route_Sea_Top
Subject To
_C1: Route_Sea_Chi + Route_Sea_NY + Route_Sea_Top <= 350
_C2: Route_SD_Chi + Route_SD_NY + Route_SD_Top <= 600
_C3: Route_SD_Chi + Route_Sea_Chi >= 325
_C4: Route_SD_NY + Route_Sea_NY >= 300
_C5: Route_SD_Top + Route_Sea_Top >= 275
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
