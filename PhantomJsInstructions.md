# General Instructions on how to install phantomjs

Please follow instructions for your operating systems below

# Ubuntu

Before installing PhantomJS, you will need to install some required packages on your system. You can install all of them with the following command:

`sudo apt-get install build-essential chrpath libssl-dev libxft-dev libfreetype6-dev libfreetype6 libfontconfig1-dev libfontconfig1 -y`
Next, you will need to download the PhantomJS. You can download the latest stable version of the PhantomJS from their official website. Run the following command to download PhantomJS:

`sudo wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2`
Once the download is complete, extract the downloaded archive file to desired system location:

`sudo tar xvjf phantomjs-2.1.1-linux-x86_64.tar.bz2 -C /usr/local/share/`
Next, create a symlink of PhantomJS binary file to systems bin directory:

`sudo ln -s /usr/local/share/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin/`

# Windows

Download phantomjs from `http://phantomjs.org/download.html`

Move the contents of `phantomjs-x.y.z-windows` to `C:\bin\phantomjs`

Add `C:\bin\phantomjs` to `PATH`

Google `add environment variable to path in windows` if you must

# OSX

You need Brew `/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
install phantomjs `brew install phantomjs`
