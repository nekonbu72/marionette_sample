import os


def setup_download_folder(dir: str):
    # dir フォルダがなければ作成
    if not os.path.isdir(dir):
        os.mkdir(dir)
        print(f"created {dir} dir")

    # dir フォルダを空にする
    ls = os.listdir(dir)
    for f in ls:
        os.remove(os.path.join(dir, f))
    print(f"cleaned up {dir} dir")
