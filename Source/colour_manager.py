class colour_list():
    def __init__(c):

        c.fullred = (255, 0, 0)
        c.fullgreen = (0, 255, 0)
        c.fullblue = (0, 0, 255)

        c.red = (155, 35, 35)
        c.green = (35, 155, 35)
        c.blue = (35, 35, 155)

        c.pink = (255, 0, 255)
        c.purple = (155, 35, 155)
        c.fullcyan = (0, 255, 255)
        c.cyan = (35, 155, 155)
        c.teal = (35, 100, 100)
        c.fullyellow = (255, 255, 0)
        c.yellow = (155, 155, 35)

        c.black = (10, 10, 10)
        c.fullblack = (1, 1, 1)

        c.white = (255, 255, 255)

        c.colourkey = (0, 0, 0)

        c.fulllist = (
            c.fullred,
            c.fullgreen,
            c.fullblue,
            c.red,
            c.green,
            c.blue,
            c.pink,
            c.purple,
            c.fullcyan,
            c.cyan,
            c.teal,
            c.fullyellow,
            c.yellow
        )

        c.primary = (
            c.fullred,
            c.fullgreen,
            c.fullblue,
            c.red,
            c.green,
            c.blue
        )

    def rand(c, choice=False):
        choice = choice.upper()

        if choice == "ALL":
            col_list = c.fulllist
        elif choice == "PRIMARY":
            col_list = c.primary

        return random.choice(col_list)


colours = colour_list()