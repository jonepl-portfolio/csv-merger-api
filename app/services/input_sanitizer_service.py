import re
import unicodedata


class InputSanitizerService:

    @staticmethod
    def sanitize_group_name(group_name: str):
        # pattern = r"[ %&()\[\]{}\/\\?+$!:@|=]+|\s+"
        pattern = r"[ %&()\[\]{}\/\\?+$!:@|=#]+|\s+"
        filtered_emoji_text = "".join(
            char
            for char in group_name
            if char.isprintable() and not unicodedata.category(char).startswith("So")
        )
        sanitized_text = re.sub(pattern, "-", filtered_emoji_text)
        sanitized_text = sanitized_text.strip("-").lower()
        return sanitized_text
