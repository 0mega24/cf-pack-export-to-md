# cf-pack-export-to-md

A project that allows for the easy conversion from a [curseforge](https://www.curseforge.com/) minecraft modpack export into a customizable text based list.

## Installation

``` shell
git clone https://github.com/0mega24/cf-pack-export-to-md.git
pip install -r requirements.txt
```

- Install python 3.11.8 or have a **.venv** setup
- You must also create a **.env** file somewhere inside of the project
- Make sure to get your own [Imgur API](https://apidocs.imgur.com/) key.
- Once you have gotten it include the line - filling in your API key

``` .env
IMGUR_API_KEY=Client-ID xxxxxxxxxxxxxxx
```

## Running

``` shell
python app.py [--log <log_level>]
```

- Use the --log argument to specify the logging level if needed. Available options are DEBUG, INFO, WARNING, ERROR, and CRITICAL with a default of WARNING.

## Frameworks Used

- [selenium](https://www.selenium.dev/) - For the webscaping of curseforge links
- [requests](https://requests.readthedocs.io/en/latest/) - For Imgur API calls
- [tqdm](https://github.com/tqdm/tqdm) - For the loading bars
- [tkinter](https://docs.python.org/3/library/dialog.html) - For the filedialog
- [typing](https://docs.python.org/3/library/typing.html) - For comprehensive type hinting

## Example Output

| Icon | Summary | Details |
| ---: | :------ | :------ |
<img src="https://i.imgur.com/DYuy6WA.png" width=48> | [**World Stripper**](https://www.curseforge.com/minecraft/mc-mods/world-stripper) <sup>[*World-Stripper-1.6.0-1.12.2.jar*](https://www.curseforge.com/minecraft/mc-mods/world-stripper/files/2635454)</sup> by **EwyBoy** <sub><sup>MIT License</sup></sub><br>Strips away blocks to reveal the underground world gen. A must have tool for all devs. dev ore map strip world | <sup>Project:250603</sup><br><sup>File:2635454</sup>
<img src="https://i.imgur.com/TrnXYbq.png" width=48> | [**IC2 Tweaker**](https://www.curseforge.com/minecraft/mc-mods/ic2-tweaker) <sup>[*ic2-tweaker-0.2.1+build.4.jar*](https://www.curseforge.com/minecraft/mc-mods/ic2-tweaker/files/4136686)</sup> by **tttusk** <sub><sup>Public Domain</sup></sub><br>CraftTweaker (for Minecraft 1.12.+) support for IC2-experimental | <sup>Project:311846</sup><br><sup>File:4136686</sup>
<img src="https://i.imgur.com/FyUyY6G.png" width=48> | [**Sit**](https://www.curseforge.com/minecraft/mc-mods/sit) <sup>[*sit-1.12.2-v1.3.jar*](https://www.curseforge.com/minecraft/mc-mods/sit/files/2848862)</sup> by **bl4ckscor3** <sub><sup>MIT License</sup></sub><br>Allows you to sit on slabs and stairs. | <sup>Project:278717</sup><br><sup>File:2848862</sup>
<img src="https://i.imgur.com/Ts3326F.png" width=48> | [**LittleTiles**](https://www.curseforge.com/minecraft/mc-mods/littletiles) <sup>[*LittleTiles_v1.5.68_mc1.12.2.jar*](https://www.curseforge.com/minecraft/mc-mods/littletiles/files/4399700)</sup> by **CreativeMD** <sub><sup>GNU Lesser General Public License version 2.1 (LGPLv2.1)</sup></sub><br>#BuildItYourself | <sup>Project:257818</sup><br><sup>File:4399700</sup>
<img src="https://i.imgur.com/VKVl5cn.png" width=48> | [**Oxygen: Market**](https://www.curseforge.com/minecraft/mc-mods/oxygen-market) <sup>[*oxygen-market-1.12.2-0.11.2.jar*](https://www.curseforge.com/minecraft/mc-mods/oxygen-market/files/2983953)</sup> by **austeretony** <sub><sup>All Rights Reserved</sup></sub><br>Global market for players to buy and sell items. | <sup>Project:342390</sup><br><sup>File:2983953</sup>

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
