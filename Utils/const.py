import json
def fix_encoding(text):
    return (text.replace("È˜", "Ș")
            .replace("Èš", "Ț")
            .replace("Ä‚", "Ă")
            .replace("Ã‚", "Â")
            .replace("Î", "Î")
            .replace("È", "Ț")
            .replace("Ä", "Ă")
            .replace("Š", "Ț"))

with open('./Utils/Region/corrected_regions.json', 'r', encoding='utf-8') as file:

        REGIONS_DATA = {
            fix_encoding(key): fix_encoding(value) if isinstance(value, str) else value
            for key, value in json.load(file).items()
        }
