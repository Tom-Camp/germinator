
color: list[tuple] = [
    (0, 70, 255),
    (0, 70, 255),
    (0, 70, 255),
    (241, 0, 0),
    (241, 0, 0),
    (241, 0, 0),
    (177, 0, 0),
    (177, 0, 0),
    (163, 255, 0),
]

phases: dict = {
    "germination": {
        "temperature": (21, 24),
        "humidity": (75, 95),
        "duration": (6, 20)
    },
    "seedling": {
        "temperature": (18, 24),
        "humidity": (70, 75),
        "duration": (9, 23),
    },
    "sprout": {
        "temperature": (18, 27),
        "humidity": (60, 70),
        "duration": (9, 23),
    },
    "vegetative": {
        "temperature": (21, 30),
        "humidity": (50, 60),
        "duration": (9, 23),
    },
}
