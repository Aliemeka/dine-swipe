import random
import string
import hashlib

def generate_shortcode() -> str:
    def gen_subsection():
        return "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(4)
        )

    shortcode = f"{gen_subsection()}_{gen_subsection()}"
    return shortcode


def generate_session_from_ip(ip: str) -> str:
    hash = hashlib.shake_256(bytes(ip, "utf-8"))
    return hash.hexdigest(20)
