import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as mpl
import os

# Build the path relative to THIS file
HERE = os.path.dirname(__file__)
font_path = os.path.join(HERE, "styles", "fonts", "GeistMono-Regular.ttf")

# Register the font with Matplotlib
fm.fontManager.addfont(font_path)

# Get the internal font name (required!)
font_prop = fm.FontProperties(fname=font_path)
font_name = font_prop.get_name()

# Set globally
mpl.rcParams["font.family"] = font_name

plt.style.use(os.path.join(HERE, "styles", "themes", "rose-pine-dawn.mplstyle"))

plt.plot([1, 2, 3])
plt.title("Geist Mono in Matplotlib")
plt.show()
