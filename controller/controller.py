import os
import sys

package_path = os.path.dirname(os.path.abspath(__file__))
h, _ = os.path.split(package_path)
sys.path.append(h)
