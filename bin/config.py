class COLORS:
    header = "\033[4m"
    red = "\033[31m"
    green = "\033[32m"
    blue = "\033[34m"
    normal = "\033[0m"


def format_verse(reference, text) -> str:
    return "{blue}{reference}{normal} \n{verse}\n".format(
        blue=COLORS.blue, reference=reference,
        normal=COLORS.normal, verse=text
    )


def format_reference(reference) -> str:
    return "{blue}{reference}{normal}".format(blue=COLORS.blue,
                                              reference=reference, normal=COLORS.normal)


def format_header(text) -> str:
    return "\n{header}{text}{normal}\n".format(header=COLORS.header, text=text, normal=COLORS.normal)
