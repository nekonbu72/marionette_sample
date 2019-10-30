import getpass
import pathlib


def profile_dir() -> str:
    user = getpass.getuser()
    profiles_dir = f"C:\\Users\\{user}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\"
    p = pathlib.Path(profiles_dir)
    if p.is_dir():
        for profile in p.iterdir():
            if profile.is_dir():
                if "default" in profile.name.lower():
                    return str(profile)
    return ""

# PROFILE = "C:\\Users\\s150209\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\5332jmf7.default"  # 会社PC
# PROFILE = "C:\\Users\\Tomoyuki Nakamura\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\2wsrx870.Default User"  # 自宅PC
