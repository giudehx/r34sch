# R34Sch - Rule 34 CLI

`r34sch` is a cli utility for downloading rule 34 content (rule34.xxx) to your device.

## Installation

### PC (Windows, Linux...)

Prerequisites:
- Python (python.org)
- Git (git-scm.com)

Open the terminal, on Windows it's `Win+R` and type `cmd`, then press enter

If you have `git` installed on your device, type:
``` git clone https://github.com/giudehx/r34sch.git ```

Go to the `r34sch` directory, where there are all of the python .py files
Ensure that you have Python installed and you clicked `Add Python on PATH` during installation
Then, type on the terminal:

``` pip install -r requirements.txt ```
or if that doesn't work:
``` python3 -m pip install -r requirements.txt ```

Now that you've installed the dependencies, you actually need to have a `.env` file, containing the Rule34.xxx cookies,
the format of the .env file is this:
```R34_COOKIE="<your rule 34 cookie>"```

To get the cookies from your browser (for this example we're doing Chrome/Edge), do these steps:
1. Go to rule34.xxx and accept the cookies (by searching something random)
2. Press `F12`. Or `Right-click`, then Inspect.
3. Go to `Application` (or `Storage`)
4. Under `Cookies`, select the site's domain (in this case: rule34.xxx)
5. You'll see a string of text, copy the whole text and paste it to the previously mentioned .env file.

If you do not want to do all of this, you can simply do when everytime you run r34sch:
```python3 r34sch.py -t```
or
```python3 r34sch.py --thumbnail```
This disables the higher quality images/videos and downloads the thumbnail/preview image instead.

*Note: only parsing videos require cookies, ive not programmed a --only-images option, yet. Oh well, i just let this exist online*

### Android/Termux

1. Install Termux on the Play Store
2. Once installed, open Termux and run: ```pkg update && pkg upgrade -y```
3. Once finished, type: ```pkg install python clang rust make pkg-config git -y```
4. Once finished, clone the repository: ``` git clone https://github.com/giudehx/r34sch.git ```
5. Then go to the repository directory by typing ```cd r34sch```
6. Type ```pip install -r requirements.txt```

You'd still need the .env file mentioned earlier, but if you don't want to do this, you can always do ```python3 r34sch.py -t```

## Using R34Sch

To run R34Sch, type (both pc and termux): ```python3 r34sch.py```, then you insert a prompt between quotes:

```python3 r34sch.py "example"```

Or options:

```python3 r34sch.py "example" <options>```

Here's the available options:

  -h, --help           show the help message and exit
  
  -i, --images IMAGES  The amount of images to download
  
  -p, --page PAGE      Tell the program what page to search
  
  -t, --thumbnail      Only download the thumbnail instead of the post image, helps speed the program
  
  -o, --output OUTPUT  Where the files will be downloaded (a folder) (default named r34out)
  
  -q, --quiet          Disables output when running R34Sch.

*Note: if using termux, and you didnt specify -o to be ``` -o /storage/...```, to view the content type `termux-setup-storage` it should be available on the default android file browser by clicking the top-left corner and scrolling down until you spot 'termux'*

## Notes
This is a very work in progress, later we'll add improvements such as different sites and api keys, multitasking as well.

