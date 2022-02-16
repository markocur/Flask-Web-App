# This application was created thanks to help and support from Corey Schafer tutorials
# Corey Schafer YouTube channel: https://www.youtube.com/c/Coreyms

# Thanks to the package structure I can avoid circular import error

from travel import app

if __name__ == '__main__':
    app.run(debug=True)