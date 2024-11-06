from pwn import *
import os, stat
import click
from colorama import Fore

context(os="linux", arch="amd64", log_level="error")

"""def set_context(system, architecture, log):
    system = system
    architecture = architecture
    log = log
    return context(os=system, arch=architecture, log_level=log)"""


def shellcoder(filename, hex):
    try:
        file = ELF(filename)
    except FileNotFoundError as e:
        print(f"{Fore.RED}[-] Error: {Fore.MAGENTA}{e}")
        exit()

    try:
        shellcode = file.section(".text")
        if hex == True:
            print(f"{Fore.LIGHTGREEN_EX}[+] Success! Here's your code:")
            print(f"{Fore.LIGHTYELLOW_EX}{shellcode.hex()}{Fore.GREEN}")
        else:
            print(shellcode)
        #print("%d bytes - Found NULL byte" % len(shellcode)) if [i for i in shellcode if i == 0] else print("%d bytes - No NULL bytes" % len(shellcode))
        print(f"{Fore.LIGHTBLUE_EX}Shellcode length: {len(shellcode)} bytes")
        if 0 in shellcode:
            print(f"{Fore.LIGHTRED_EX}[!!] Warning: Found NULL byte")
        else:
            print(f"{Fore.LIGHTGREEN_EX}[+] No NULL bytes!")
    except Exception as e:
        print(f"{Fore.RED}[-] Error: {Fore.MAGENTA}{e}")



def loader(shellcode):
    if shellcode:
        try:
            run_shellcode(unhex(shellcode)).interactive()
        except Exception as e:
            print(f"{Fore.RED}[-] Error: {Fore.MAGENTA}{e}")
    else:
        print(f"{Fore.RED}[-] Error: Could not parse shellcode. Please provide a valid hex string.")


def assembler(shellcode, filename):
    if shellcode and filename:
        try:
            ELF.from_bytes(unhex(shellcode)).save(filename)
            os.chmod(filename, stat.S_IREAD|stat.S_IWRITE|stat.S_IEXEC)
            print(f"{Fore.LIGHTGREEN_EX}[+] Success: Code successfully assembled to {Fore.CYAN}./{filename}")
        except Exception as e:
            print(f"{Fore.RED}[-] Error: {Fore.MAGENTA}{e}")
    elif not shellcode:
        print(f"{Fore.RED}[-] Error: Could not parse shellcode. Please provide a valid hex string.")
    elif not filename:
        print(f"{Fore.RED}[-] Error: Could not create file. Please provide a valid filename.")
    else:
        print(f"{Fore.RED}[-] Error: Could not parse shellcode or filename. Please provide a valid hex string and filename to write.")


@click.group()
def cli():
    print(f"""{Fore.YELLOW}
        ⠀⠀⠀⠀⣀⣤⣴⣶⣶⣶⣦⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⢿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀            
        ⢀⣾⣿⣿⣿⣿⣿⣿⣿⣅⢀⣽⣿⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀
        ⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⠁⠀⠀⣴⣶⡄⠀⣶⣶⡄⠀⣴⣶⡄
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣀⠀⠙⠋⠁⠀⠉⠋⠁⠀⠙⠋⠀
        ⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀         
        ⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠈⠙⠿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
             _       _          _ _  
            | |     | |        | | | 
   ___  __ _| |_ ___| |__   ___| | | 
  / _ \/ _` | __/ __| '_ \ / _ \ | | 
 |  __/ (_| | |_\__ \ | | |  __/ | | 
  \___|\__,_|\__|___/_| |_|\___|_|_| 
    """)
    print(f"""{Fore.YELLOW}
Creator: sapphicart
          
Usage: eatshell [COMMAND] options [ARGUMENTS]

Commands:
          
    shellcode
        --file <filename> --hex <boolean>
        Use this command to load an ELF file and extract shellcode. 
        Turn --hex True for hex encoding.
          
    load
        --shellcode <hex string>
        Use this command to run the provided shellcode interactively. 
        Use with caution, might not work everytime.
          
    assemble
        --shellcode <hex string> --file <filename>
        Use this command to assemble given shellcode into an
        ELF file with rwx permissions for the owner.
          

    """)


@click.command()
@click.option('--file', help="Enter the filename to extract shellcode.")
@click.option('--hex', help="Turn hex mode on/off with --hex True/False.", type=bool)
def shellcode(file, hex):
    shellcoder(file, hex)


@click.command()
@click.option('--shellcode', type=str, help="Enter the shellcode as a hex string.")
def load(shellcode):
    loader(shellcode)


@click.command()
@click.option('--shellcode', help="Enter the shellcode as a hex string.")
@click.option('--file', help="Enter the output filename.")
def assemble(shellcode, file):
    assembler(shellcode, file)


if __name__=='__main__':
    cli.add_command(load)
    cli.add_command(shellcode)
    cli.add_command(assemble)
    cli()