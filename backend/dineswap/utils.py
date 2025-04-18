import random
import string


def generate_shortcode():
    def gen_subsection():
        return "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(4)
        )

    shortcode = f"{gen_subsection()}-{gen_subsection}"
    return shortcode
