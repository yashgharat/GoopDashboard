from pyowm.owm import OWM

mgr = OWM('6a960e5cb18eef95b84c64f8677103c2').weather_manager()

one_call = mgr.one_call(lat = 28.6024, lon = 81.2001)

print(one_call)
