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

Go to the `r34sch` directory (`cd r34sch` on terminal), where there are all of the python .py files

Ensure that you have Python installed and you clicked `Add Python on PATH` during installation

Then, type on the terminal:

``` pip install -r requirements.txt ```
or if that doesn't work:
``` python3 -m pip install -r requirements.txt ```

Now that you've installed the dependencies, you actually need to have a `r34sch.cfg` file, containing the Rule34.xxx API Key and User ID. **It's highly recommended to do this.**

The format of the config file is this:

```
api_key=<YOUR_API_KEY>
user_id=<YOUR_USER_ID>
cookies=<YOUR_RULE34_COOKIES>
```

To get the API Key (and User ID) (skip 1 and 2 if you are already logged in):
1. Go to https://rule34.xxx and click on `My Account`
2. Click `Sign Up` and create an account, or click `Login` if you have an account
3. Once logged in, click `Options`, scroll down until you see `API Access Credentials`
4. Check the box that says `Generate New Key?`, then click `Save` at the bottom of the page.
5. Now scroll to `API Access Credentials` again, and you'll see the API Key in plain text. **Do not close the browser.**

It should look like this: *this is just an example lookalike*

```
&api_key=abc123...&user_id=xxxxxx
```

Now how to configure R34Sch?
1. At the same directory as `r34sch.py` create a new file, it has to be exactly named `r34sch.cfg`
2. At the settings page of rule 34 copy the value after `&api_key=`. **Do not copy `&user_id=` and the value that comes after it, stop at the ampersand (&)**
3. At the `r34sch.cfg` file, type: `api_key=` as the first thing, then after the equal sign paste the api key. Do not save the file yet.
4. Go to the settings page of rule 34 copy the value after `&user_id=`.
5. At the config file again type: `user_id=`, then after the equal sign paste the user id.
The .cfg file now should look like this:
```
api_key=<YOUR_API_KEY>
user_id=<YOUR_USER_ID>
```
6. Save the file.
7. Since you should be at the same directory as `r34sch.py` script, type:
```
python r34sch.py --load-config
```
If it errors because it couldn't find `r34sch.cfg`, make sure that the file you just saved should be exactly named (both filename and extension): `r34sch.cfg`. Then try again

**Congrats! Now it's much more faster! I hope it wasn't a pain in the ass!**

If you do not want to do all of this, you can simply skip all of this and run it as is.

*Note: only parsing videos require cookies, ive not programmed a --only-images option, yet. Oh well, i just let this exist online*

### Android/Termux

1. Install Termux on the Play Store
2. Once installed, open Termux and run: ```pkg update && pkg upgrade -y```
3. Once finished, type: ```pkg install python clang rust make pkg-config git -y```
4. Once finished, clone the repository: ``` git clone https://github.com/giudehx/r34sch.git ```
5. Then go to the repository directory by typing ```cd r34sch```
6. Type ```pip install -r requirements.txt```

**Note: if you encounter problems installing the package 'Pillow', copy this command and run it on termux:**
```bash
LDFLAGS="-L/system/lib64/" CFLAGS="-I$PREFIX/include" pip install Pillow
```

Then install dependencies again:
```bash
pip install -r requirements.txt
```

You'd still need the r34sch_config.cfg file mentioned earlier, but if you don't want to do this, you can always run it as is.

## Using R34Sch

To run R34Sch, type (both pc and termux): ```python3 r34sch.py```, then you insert a prompt between quotes:

```python3 r34sch.py "example"```

Or options:

```python3 r34sch.py "example" <options>```

Here's the available options:
```

  -h, --help           show the help message and exit
  
  -i, --images IMAGES  The amount of images to download
  
  -p, --page PAGE      Tell the program what page to search
  
  -t, --thumbnail      Only download the thumbnail instead of the post image, helps speed the program
  
  -o, --output OUTPUT  Where the files will be downloaded (a folder) (default named r34out)
  
  -q, --quiet          Disables output when running R34Sch.
  
  --skip-metadata      Disable writing metadata when downloading files.
  
  --exclude-ai         Filter AI posts. Rejects a post from downloading if in one of its tags containes 'ai_'.

```

*Note: if using termux, and you didnt specify -o to be ``` -o /sdcard/...```, to view the content type `termux-setup-storage` it should be available on the default android file browser by clicking the top-left corner and scrolling down until you spot 'termux'*

## Notes
This is a very work in progress, later we'll add improvements such as different sites and api keys, multitasking as well.
