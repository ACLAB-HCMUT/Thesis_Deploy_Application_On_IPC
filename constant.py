# relay_ON = [
#     [1, 6, 0, 0, 0, 255, 201, 138],
#     [2, 6, 0, 0, 0, 255, 201, 185],
#     [3, 6, 0, 0, 0, 255, 200, 104],
#     [4, 6, 0, 0, 0, 255, 201, 223],
#     [5, 6, 0, 0, 0, 255, 200, 14],
#     [6, 6, 0, 0, 0, 255, 200, 61],
#     [7, 6, 0, 0, 0, 255, 201, 236],
#     [8, 6, 0, 0, 0, 255, 201, 19]
# ]

# relay_OFF = [
#     [1, 6, 0, 0, 0, 0, 137, 202],
#     [2, 6, 0, 0, 0, 0, 137, 249],
#     [3, 6, 0, 0, 0, 0, 136, 40],
#     [4, 6, 0, 0, 0, 0, 137, 159],
#     [5, 6, 0, 0, 0, 0, 136, 78],
#     [6, 6, 0, 0, 0, 0, 136, 125],
#     [7, 6, 0, 0, 0, 0, 137, 172],
#     [8, 6, 0, 0, 0, 0, 137, 83]
# ]

# constant.py
relay_ON = {
    0: b'\x01\x0F\x00\x00\x00\x08\x01\xFF\xBE\xD5',  # Bật relay all
    1: b'\x01\x05\x00\x00\xFF\x00\x8C\x3A',  # Bật relay 1
    2: b'\x01\x05\x00\x01\xFF\x00\xDD\xFA',  # Bật relay 2
    3: b'\x01\x05\x00\x02\xFF\x00\x2D\xFA',  # Bật relay 3
    4: b'\x01\x05\x00\x03\xFF\x00\x7C\x3A'   # Bật relay 4
}

relay_OFF = {
    0: b'\x01\x0F\x00\x00\x00\x08\x01\x00\xFE\x95',  # Bật relay all
    1: b'\x01\x05\x00\x00\x00\x00\xCD\xCA',  # Tắt relay 1
    2: b'\x01\x05\x00\x01\x00\x00\x9C\x0A',  # Tắt relay 2
    3: b'\x01\x05\x00\x02\x00\x00\x6C\x0A',  # Tắt relay 3
    4: b'\x01\x05\x00\x03\x00\x00\x3D\xCA'   # Tắt relay 4
}

# AIO_USERNAME_ADAFRUIT = "Vinhnguyen20"
# AIO_KEY_ADAFRUIT = "aio_KurW86etHXmNabVgDFcauPP9y80j"

ADAFRUIT_AIO_USERNAME = "Vinhnguyen2003"
ADAFRUIT_AIO_KEY      = "aio_wlvG09B8h1VY7PBP0bVCBHq9SoeX"

# relay1_ON  = [1, 6, 0, 0, 0, 255, 201, 138]
# relay1_OFF = [1, 6, 0, 0, 0, 0, 137, 202]

# relay2_ON  = [2, 6, 0, 0, 0, 255, 201, 185]
# relay2_OFF = [2, 6, 0, 0, 0, 0, 137, 249]

# relay3_ON  = [3, 6, 0, 0, 0, 255, 200, 104]
# relay3_OFF = [3, 6, 0, 0, 0, 0, 136, 40]

# relay4_ON  = [4, 6, 0, 0, 0, 255, 201, 223]
# relay4_OFF = [4, 6, 0, 0, 0, 0, 137, 159]

# relay5_ON  = [5, 6, 0, 0, 0, 255, 200, 14]
# relay5_OFF = [5, 6, 0, 0, 0, 0, 136, 78]

# relay6_ON  = [6, 6, 0, 0, 0, 255, 200, 61]
# relay6_OFF = [6, 6, 0, 0, 0, 0, 136, 125]

# relay7_ON  = [7, 6, 0, 0, 0, 255, 201, 236]
# relay7_OFF = [7, 6, 0, 0, 0, 0, 137, 172]

# relay8_ON  = [8, 6, 0, 0, 0, 255, 201, 19]
# relay8_OFF = [8, 6, 0, 0, 0, 0, 137, 83