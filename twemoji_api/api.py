from pathlib import Path
from emoji_data_python import char_to_unified


def get_extension_folder(extension: str):
    if extension == "svg":
        folder = "svg"
    elif extension == "png":
        folder = "72x72"
    else:
        raise ValueError("Invalid extension.")
    return Path(__file__).parent.absolute() / f"assets/{folder}"


def _get_path_from_unified(folder: Path, unified: str, extension: str):
    # 1. Try exact match
    path = folder / f"{unified}.{extension}"
    if path.exists():
        return path

    # 2. Try removing leading zeros
    parts = unified.split("-")
    unified_no_zeros = "-".join([p.lstrip("0") if p != "0" else "0" for p in parts])
    path = folder / f"{unified_no_zeros}.{extension}"
    if path.exists():
        return path

    # 3. Fallback: remove variation selectors (fe0f)
    if "fe0f" in parts:
        parts_no_vs = [p for p in parts if p != "fe0f"]
        unified_no_vs = "-".join(parts_no_vs)
        # Try both with and without zeros for the version without VS
        res = _get_path_from_unified(folder, unified_no_vs, extension)
        if res:
            return res

    # 4. Aggressive fallback: for ZWJ sequences, try the base emoji
    if "200d" in parts:
        # Try taking components from left to right
        for i in range(len(parts) - 1, 0, -1):
            if parts[i] == "200d":
                base_unified = "-".join(parts[:i])
                res = _get_path_from_unified(folder, base_unified, extension)
                if res:
                    return res

    return None


def get_emoji_path(emoji: str, extension: str = "png"):
    folder = get_extension_folder(extension)
    unified = char_to_unified(emoji).lower()
    
    path = _get_path_from_unified(folder, unified, extension)

    if path:
        return path
    else:
        raise ValueError("Emoji not found.")


def get_emoji_url(emoji, extension = "png"):
    path = get_emoji_path(emoji, extension)
    if path is None:
        return None
    folder = path.parent.name
    return f"https://raw.githubusercontent.com/jdecked/twemoji/master/assets/{folder}/{path.name}"
